import os
import json
import time
import threading
import queue
import sys

from saveparser import CelesteSaveData


def check_settings():
    if os.path.isfile("./settings.json"):
        # settings file exists
        with open("./settings.json", "r") as f:
            return json.loads(f.read())
    else:
        result = input("No settings.json found, create settings file now? (y/n)")
        if result == "y":
            settings = {}
            settings["CelesteSaveFolder"] = input("Path to your Celeste saves folder: ")
            settings["ILSaveSlot"] = input("Save slot you do IL runs on: ")
            settings["AnyPercentSaveSlot"] = input("Save slot for any% runs: ")
            with open("./settings.json", "w") as f:
                f.write(json.dumps(settings))
                return settings
        else:
            print("Process will exit now.")
            quit()


def monitor_file_for_changes(path, interval, callback):
    last_time = 0
    last_data = ""
    while True:
        now = time.time()
        new_data = last_data
        if not os.path.isfile(path):
            new_data = ""
        elif os.path.getmtime(path) > last_time:
            # file was modified since we last checked
            with open(path, "r") as f:
                new_data = f.read()
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


def main():
    # check if settings exists
    settings = check_settings()
    
    il_file_queue = queue.Queue()
    anypercent_file_queue = queue.Queue()

    il_file_path = save_path_from_slot(settings["CelesteSaveFolder"], settings["ILSaveSlot"])
    il_file_checker = threading.Thread(
        target=monitor_file_for_changes,
        args=(il_file_path, 0.1, il_file_queue.put))
    il_file_checker.daemon = True
    il_file_checker.start()

    anypercent_file_path = save_path_from_slot(settings["CelesteSaveFolder"], settings["AnyPercentSaveSlot"])
    anypercent_file_checker = threading.Thread(
        target=monitor_file_for_changes,
        args=(anypercent_file_path, 0.1, anypercent_file_queue.put))
    anypercent_file_checker.daemon = True
    anypercent_file_checker.start()

    while True:
        try:
            new_il_save = il_file_queue.get_nowait()
            print(new_il_save)
        except queue.Empty:
            print("empty queue")
        time.sleep(0.1)
    quit()


if __name__ == "__main__":
    main()
