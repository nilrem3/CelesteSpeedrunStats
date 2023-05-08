import queue

LOGGING_LEVEL_PREFIXES = {
    0: "\u001b[0;34m[INFO]\u001b[0m",
    1: "\u001b[0;33m[WARN]\u001b[0m",
    2: "\u001b[0;31m[ERROR]\u001b[0m",
    3: "\u001b[41m\u001b[1;37m[FATAL]\u001b[0m"
}

class LogLevel:
    INFO = 0
    WARN = 1
    ERROR = 2
    FATAL = 3

logging_queue = queue.Queue()


class LogMessage:
    def __init__(self, loglevel: int, message: str):
        self.loglevel = loglevel
        self.message = message

    def get_display_text(self):
        return LOGGING_LEVEL_PREFIXES[self.loglevel] + " " + self.message
