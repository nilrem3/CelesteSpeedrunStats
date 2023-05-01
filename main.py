import os
import json
import time

def check_settings():
    if os.path.isfile("./settings.json"):
        #settings file exists
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
            #file was modified since we last checked
            with open(path, "r") as f:
                new_data = f.read()
        if new_data != last_data:
            callback(new_data)
            last_data = new_data
        last_time = now
        time.sleep(interval)


def main():
    #check if settings exists
    settings = check_settings()
    

if __name__ == "__main__":
    main()
