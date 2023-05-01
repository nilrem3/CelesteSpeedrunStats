import os
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import re

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

class SaveHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        event_type, src_path = event.event_type, event.src_path
        print(event_type, src_path)

            

def main():
    #check if settings exists
    settings = check_settings()

    observer = Observer()
    event_handler = SaveHandler()

    observer.schedule(event_handler, settings["CelesteSaveFolder"], recursive=False)
    observer.start()
    input("Type any key to stop")
    observer.stop()
    

if __name__ == "__main__":
    main()
