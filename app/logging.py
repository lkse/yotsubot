import logging
import config
import colorlog

logger = logging.getLogger()


def setup_logging():
    """
    Sets up logging for the bot.
    Creates a logger, sets the format, and adds a handler for the console
    with colored output.
    """

    logger.setLevel(logging.INFO)

    logformat = "%(asctime)s %(levelname)-8s %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"

    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter(
            reset=True,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            },
            secondary_log_colors={},
            style='%'
        ))

    logger.addHandler(handler)
    filename = f"{config.Dir}\\logs\\log.log"
    file_handler = logging.FileHandler(filename)
    file_handler.setFormatter(logging.Formatter(logformat, datefmt))
    logger.addHandler(file_handler)
