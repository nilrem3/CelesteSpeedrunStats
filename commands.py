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
        case ["threshold", "deaths", num]:
            try:
                il_uploader.death_threshold = int(num)
            except ValueError:
                log_message(LogLevel.ERROR, f"{num} is not a valid number.")
        case ["threshold", "time", num]:
            try:
                il_uploader.time_threshold = int(num)
            except ValueError:
                log_message(LogLevel.ERROR, f"{num} is not a valid number")
        case ["tag", "add", *tags]:
            for tag in " ".join(tags).split(", "):
                if tag not in il_uploader.tags:
                    il_uploader.tags.append(tag)
        case ["tag", "list"]:
            print("Current tags: " + ", ".join(il_uploader.tags))
        case ["tag", "clear"]:
            il_uploader.tags = []
            log_message(LogLevel.OK, "Tags Cleared")