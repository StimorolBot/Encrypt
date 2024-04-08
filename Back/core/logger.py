import logging


class ColoredFormatter(logging.Formatter):
    COLORS = {'DEBUG': '\033[94m', 'INFO': '\033[92m', 'WARNING': '\033[93m',
              'ERROR': '\033[91m', 'CRITICAL': '\033[95m'}

    def format(self, record):
        log_fmt = f"{self.COLORS.get(record.levelname)}%(levelname)s:   \033[97m %(message)s"
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class CustomLogger(ColoredFormatter):
    def __init__(self, loger_name: str, path):
        super().__init__()
        self.path = path
        self.logger = logging.getLogger(name=loger_name)
        self.logger.setLevel(logging.DEBUG)
        self.format = "%(levelname)s:    %(asctime)s -> %(message)s"

        self.terminal_log = logging.StreamHandler()
        self.terminal_log.setLevel(logging.DEBUG)
        self.terminal_log.setFormatter(ColoredFormatter())
        self.logger.addHandler(self.terminal_log)

        self.file_log = logging.FileHandler(filename=self.path)
        self.file_log.setLevel(logging.INFO)
        self.file_log.setFormatter(logging.Formatter(self.format))
        self.logger.addHandler(self.file_log)


CustomLogger(loger_name="user_logger", path="core/.log/user.log")
CustomLogger(loger_name="encrypt_logger", path="core/.log/encrypt.log")

user_logger = logging.getLogger("user_logger")
encrypt_logger = logging.getLogger("encrypt_logger")
