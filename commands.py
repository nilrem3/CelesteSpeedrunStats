import constants
from logging_system import log_message, LogLevel


def parse_command(command, il_uploader):
    match command.split():
        case ["quit"]:
            quit()
        case ["help", "advanced"]:
            print(constants.ADVANCED_HELP_MESSAGE)
        case ["help"]:
            print(constants.HELP_MESSAGE)
        case ["setloglevel", level]:
            try:
                LogLevel.current = int(level)
            except ValueError:
                log_message(
                    LogLevel.ERROR,
                    f"{level} is not a valid loglevel. Choose a number between 0 and 4 (inclusive).",
                )
        case ["practice", *args]:
            parse_practice_command(args, il_uploader)
        case ["tag", "add", *tags]:
            for tag in " ".join(tags).split(", "):
                if tag not in il_uploader.tags:
                    il_uploader.tags.append(tag)
        case ["tag", "list"]:
            print("Current tags: " + ", ".join(il_uploader.tags))
        case ["tag", "clear"]:
            il_uploader.tags = []
            log_message(LogLevel.OK, "Tags Cleared")
        case ["comment", *words]:
            comment = " ".join(words)
            il_uploader.add_comment(comment)
        case ["category", *new_cat]:
            new_cat = " ".join(new_cat)
            success = il_uploader.set_category(new_cat)
            if success:
                log_message(LogLevel.OK, f"Category changed to {new_cat}")
            else:
                log_message(LogLevel.ERROR, f"{new_cat} is not a valid category.")
        case _:
            log_message(
                LogLevel.ERROR,
                f"'{command}' is not a recognized command, use 'help' to see valid commands.",
            )


def parse_practice_command(args, il_uploader):
    match args:
        case []:
            print(constants.PRACTICE_HELP_MESSAGE)
        case ["on"]:
            il_uploader.practice_mode = "on"
            log_message(LogLevel.OK, "All runs will be marked as practice")
        case ["off"]:
            il_uploader.practice_mode = "off"
            log_message(LogLevel.OK, "Runs will never be marked as practice")
        case ["auto"]:
            il_uploader.practice_mode = "auto"
            log_message(
                LogLevel.OK,
                "Runs will be marked as practice if they meet practice auto thresholds",
            )
        case ["auto", "deaths", num]:
            try:
                il_uploader.death_threshold = int(num)
                il_uploader.practice_mode = "auto"
                log_message(
                    LogLevel.OK,
                    f"Runs with more than {num} deaths will be marked as practice",
                )
            except ValueError:
                log_message(LogLevel.ERROR, f"{num} is not a valid number.")
        case ["auto", "time", num]:
            try:
                il_uploader.time_threshold = int(num)
                il_uploader.practice_mode = "auto"
                log_message(
                    LogLevel.OK,
                    f"Runs longer than {num} seconds will be marked as practice",
                )
            except ValueError:
                log_message(LogLevel.ERROR, f"{num} is not a valid number")
        case ["auto", "list"]:
            log_message(
                LogLevel.INFO,
                f"Practice thresholds:\ntime threshold: {il_uploader.time_threshold}\ndeath threshold: {il_uploader.death_threshold}",
            )
        case ["auto", "clear"]:
            il_uploader.death_threshold = None
            il_uploader.time_threshold = None
            log_message(
                LogLevel.OK,
                "Auto practice thresholds cleared",
            )
        case ["auto", "clear", "time"]:
            il_uploader.time_threshold = None
            log_message(
                LogLevel.OK,
                "Auto practice time threshold cleared",
            )
        case ["auto", "clear", "deaths"]:
            il_uploader.death_threshold = None
            log_message(
                LogLevel.OK,
                "Auto practice deaths threshold cleared",
            )
        case _:
            log_message(
                LogLevel.ERROR,
                "Invalid practice command, use 'practice' to learn more",
            )
