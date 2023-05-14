import os
import json
import time
import threading
import queue
from logging_system import LogLevel, log_message
from saveparser import CelesteSaveData
from individualleveldata import CelesteIndividualLevelData
from commands import parse_command
import settings
import constants
import uploader


def check_settings():
    settings_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "settings.json"
    )
    if os.path.isfile(settings_path):
        # settings file exists
        with open(settings_path, "r") as f:
            return fill_in_missing_settings(json.loads(f.read()))
    else:
        return fill_in_missing_settings({})


def fill_in_missing_settings(settings_object):
    settings_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "settings.json"
    )
    for s in settings.SETTINGS:
        if not s.name in settings_object:
            print(f"Setting {s.name} not found.")
            settings_object[s.name] = s.get_from_user()
    with open(settings_path, "w") as f:
        f.write(json.dumps(settings_object))
        return settings_object


def monitor_file_for_changes(path, interval, callback):
    global logging_queue
    last_time = 0
    last_data = ""
    while True:
        now = time.time()
        new_data = last_data
        if not os.path.isfile(path):
            new_data = ""
        elif os.path.getmtime(path) > last_time:
            # file was modified since we last checked
            if last_time != 0:
                log_message(LogLevel.INFO, "File update detected, reading data.")
            try:
                with open(path, "r") as f:
                    new_data = f.read()
            except PermissionError:
                log_message(
                    LogLevel.ERROR,
                    f"Failed to read file {path}, insufficient permission.".format(
                        path
                    ),
                )
                continue  # this just happens sometimes, we're not sure why, just try again next interval
        if new_data != last_data:
            callback(new_data)
            last_data = new_data
        last_time = now
        time.sleep(interval)


def save_path_from_slot(saves_dir, slot):
    return os.path.join(saves_dir, slot + ".celeste")


def print_total_file_time(xml):
    save = CelesteSaveData(xml)
    print(save.total_time_100_ns)


def input_loop(msg_queue):
    while True:
        command = input()
        msg_queue.put(command)


def main():
    # check if settings exists
    settings = check_settings()

    if not settings["ILSaveSlot"] in constants.VANILLA_SAVE_SLOTS:
        log_message(
            LogLevel.WARN,
            f"IL Save Slot (slot {settings['ILSaveSlot']}) is only accessible in Everest.",
        )
    if not settings["AnyPercentSaveSlot"] in constants.VANILLA_SAVE_SLOTS:
        log_message(
            LogLevel.WARN,
            f"Any% Save Slot (slot {settings['AnyPercentSaveSlot']}) is only accessible in Everest.",
        )

    current_log_level = 0

    il_file_queue = queue.Queue()
    anypercent_file_queue = queue.Queue()
    command_queue = queue.Queue()

    il_run_data = CelesteIndividualLevelData(settings)

    il_file_path = save_path_from_slot(
        settings["CelesteSaveFolder"], settings["ILSaveSlot"]
    )
    il_file_checker = threading.Thread(
        target=monitor_file_for_changes,
        args=(il_file_path, 0.1, il_file_queue.put),
    )
    il_file_checker.daemon = True
    il_file_checker.start()
    log_message(LogLevel.OK, f"Started IL Thread on slot {settings['ILSaveSlot']}")

    anypercent_run_data = CelesteIndividualLevelData(settings)

    anypercent_file_path = save_path_from_slot(
        settings["CelesteSaveFolder"], settings["AnyPercentSaveSlot"]
    )
    anypercent_file_checker = threading.Thread(
        target=monitor_file_for_changes,
        args=(anypercent_file_path, 0.1, anypercent_run_data.update_from_xml),
    )
    anypercent_file_checker.daemon = True
    anypercent_file_checker.start()
    log_message(
        LogLevel.OK, f"Started Any% Thread on slot {settings['AnyPercentSaveSlot']}"
    )

    command_queue = queue.Queue()
    command_reader = threading.Thread(target=input_loop, args=(command_queue,))
    command_reader.daemon = True
    command_reader.start()
    log_message(LogLevel.OK, "Started Command Thread")

    il_uploader = uploader.ILDataUploader()
    success = il_uploader.setup_sheet(settings)
    if not success:
        log_message(LogLevel.FATAL, "Failed to set up Google Sheet.")
        quit()
    else:
        log_message(LogLevel.OK, "Connected to google sheet.")

    while True:
        try:
            new_il_save = il_file_queue.get_nowait()
            il_run_data.update_from_xml(new_il_save)

            if il_run_data.ready_to_upload:
                log_message(LogLevel.INFO, "IL Run ready to upload.")
                il_uploader.upload_run_to_sheet(il_run_data)
                il_run_data.reset()

        except queue.Empty:
            pass

        while not command_queue.empty():
            try:
                command = command_queue.get_nowait()
                parse_command(command, il_uploader)
            except queue.Empty:
                break
        time.sleep(0.1)


if __name__ == "__main__":
    main()
