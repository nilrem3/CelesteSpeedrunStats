import constants
from logging_system import log_message, LogLevel


def parse_command(command, il_uploader):
    match command.split():
        case ["quit"]:
            quit()
        case ["help", *args]:
            parse_help_command(args)
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
        case ["tag", *args]:
            parse_tag_command(args, il_uploader)
        case ["comment", *words]:
            comment = " ".join(words)
            il_uploader.add_comment(comment)
            log_message(LogLevel.OK, f"Set comment of previous run to '{comment}'")
        case ["category", *args]:
            parse_category_command(args, il_uploader)
        case _:
            log_message(
                LogLevel.ERROR,
                f"'{command}' is not a recognized command, use 'help' to see valid commands.",
            )


def parse_category_command(args, il_uploader):
    match args:
        case []:
            log_message(LogLevel.INFO, f"Current category is {il_uploader.category}")
        case ["help"]:
            print(constants.CATEGORY_HELP_MESSAGE)
        case ["list"]:
            categories = ", ".join(constants.IL_CATEGORIES)
            log_message(
                LogLevel.INFO,
                f"Individual level category options include {categories}",
            )
        case ["current"]:
            log_message(LogLevel.INFO, f"Current category is {il_uploader.category}")
        case ["set", *new_cat]:
            new_cat = " ".join(new_cat)
            success = il_uploader.set_category(new_cat)
            if success:
                log_message(LogLevel.OK, f"Category changed to {il_uploader.category}")
            else:
                log_message(LogLevel.ERROR, f"{new_cat} is not a valid category.")
        case _:
            new_cat = " ".join(args)
            success = il_uploader.set_category(new_cat)
            if success:
                log_message(LogLevel.OK, f"Category changed to {il_uploader.category}")
            else:
                log_message(LogLevel.ERROR, f"{new_cat} is not a valid category.")


def parse_help_command(args):
    match args:
        case []:
            print(constants.HELP_MESSAGE)
        case ["help"]:
            print(constants.HELP_MESSAGE)
        case ["advanced"]:
            print(constants.ADVANCED_HELP_MESSAGE)
        case ["practice"]:
            print(constants.PRACTICE_HELP_MESSAGE)
        case ["tag"]:
            print(constants.TAG_HELP_MESSAGE)
        case _:
            log_message(
                LogLevel.ERROR,
                f"'{args}' is not a recognized command, use 'help' to see valid commands.",
            )


def parse_tag_command(args, il_uploader):
    match args:
        case []:
            print(constants.TAG_HELP_MESSAGE)
        case ["help"]:
            print(constants.TAG_HELP_MESSAGE)
        case ["add", *tag_data]:
            tags = " ".join(tag_data).split(", ")
            for tag in tags:
                if tag not in il_uploader.tags:
                    il_uploader.tags.append(tag)
            tag_str = ", ".join(il_uploader.tags)
            log_message(LogLevel.OK, f"Added session tags: {tag_str}")
        case ["list"]:
            tags = ", ".join(il_uploader.tags)
            log_message(LogLevel.INFO, f"Current tags: {tags}")
        case ["clear"]:
            il_uploader.tags = []
            log_message(LogLevel.OK, "Tags Cleared")
        case _:
            log_message(
                LogLevel.ERROR,
                "Invalid tag command, use 'tag' to learn more",
            )


def parse_practice_command(args, il_uploader):
    match args:
        case []:
            il_uploader.practice_mode = "on"
            log_message(LogLevel.OK, "All runs will be marked as practice")
        case ["help"]:
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
                "Invalid practice command, use 'practice help' to learn more",
            )
