class Log:
    LOG_LEVEL_NONE = 0x0
    LOG_LEVEL_FATAL = 0x1
    LOG_LEVEL_ERROR = 0x2
    LOG_LEVEL_WARN = 0x3
    LOG_LEVEL_INFO = 0x4
    LOG_LEVEL_DEBUG = 0x5
    log_level = LOG_LEVEL_WARN

    @staticmethod
    def setLogLevel(level):
        Log.log_level = level

    @staticmethod
    def fatal(log):
        if Log.log_level >= Log.LOG_LEVEL_FATAL:
            print('\033[0;31m[FATAL] ' + log + '\033[0m')

    @staticmethod
    def error(log):
        if Log.log_level >= Log.LOG_LEVEL_ERROR:
            print('\033[0;31m[ERROR] ' + log + '\033[0m')

    @staticmethod
    def warn(log):
        if Log.log_level >= Log.LOG_LEVEL_WARN:
            print('\033[0;33m[WARN] ' + log + '\033[0m')

    @staticmethod
    def info(log):
        if Log.log_level >= Log.LOG_LEVEL_INFO:
            print('[INFO] ' + log)

    @staticmethod
    def debug(log):
        if Log.log_level >= Log.LOG_LEVEL_DEBUG:
            print('[DEBUG] ' + log)