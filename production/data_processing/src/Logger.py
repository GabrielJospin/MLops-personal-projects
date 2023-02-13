import datetime
import logging


class Logger:

    def __init__(self, classe) -> None:
        super().__init__()
        logging.basicConfig(level=logging.WARNING, force=True)
        self.logger = logging.getLogger(classe)
        self.logger.setLevel(logging.INFO)

    @staticmethod
    def __treat_text(text):
        time = datetime.datetime.now()
        return f'({time}) {text}'

    def info(self, text):
        self.logger.info(self.__treat_text(text))

    def warning(self, text):
        self.logger.warning(self.__treat_text(text))

    def error(self, text):
        self.logger.error(self.__treat_text(text))
