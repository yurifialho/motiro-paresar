import logging

class Logger:
    __logger = None

    @classmethod
    def setup(cls, name : str, level : int = logging.INFO) -> None:
        logging.basicConfig(level=level)
        if level == logging.DEBUG:
            cls.__logger = logging.getLogger(name)    
        else:
            cls.__logger = logging.getLogger('TUIXAUA')
    
    @classmethod
    def info(cls, msg : str) -> None:
        cls.__logger.info(msg)

    @classmethod
    def error(cls, msg : str) -> None:
        cls.__logger.error(msg)