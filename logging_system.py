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

def log_message(log_level, msg):
    print(LOGGING_LEVEL_PREFIXES[log_level] + " " + msg)
