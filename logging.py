
LOGGING_LEVEL_PREFIXES = {
    0: "\\e[0;34m[INFO]\\e[0m",
    1: "\\e[0;33m[WARN]\\e[0m",
    2: "\\e[0;31m[ERROR]\\e[0m",
    3: "\\e[41m\\e[1;37m[FATAL]\\e[0m"
}


class LogMessage:
    def __init__(self, loglevel: int, message: str):
        self.loglevel = loglevel
        self.message = message

    def get_display_text(self):
        return LOGGING_LEVEL_PREFIXES[self.loglevel] + " " + self.message
