import logging


class LogMgr:
    app_logger: logging.Logger = None

    @classmethod
    def setup(cls, verbose=False):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname).1s] %(name)s(%(module)s:%(lineno)d) : %(message)s",
            datefmt="%I:%M:%S"
        )
        cls.app_logger = logging.getLogger('cp4')
        cls.app_logger.setLevel(logging.DEBUG if verbose else logging.INFO)

        return cls.app_logger
