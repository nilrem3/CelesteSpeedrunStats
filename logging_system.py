LOGGING_LEVEL_PREFIXES = {
    0: "\u001b[0;34m[INFO]\u001b[0m",
    1: "\u001b[0;32m[OK]\u001b[0m",
    2: "\u001b[0;33m[WARN]\u001b[0m",
    3: "\u001b[0;31m[ERROR]\u001b[0m",
    4: "\u001b[41m\u001b[1;37m[FATAL]\u001b[0m"
}

class LogLevel:
    INFO = 0
    OK = 1
    WARN = 2
    ERROR = 3
    FATAL = 4
    current = 0

def log_message(log_level, msg):
    if log_level >= LogLevel.current:
        print(LOGGING_LEVEL_PREFIXES[log_level] + " " + msg)
