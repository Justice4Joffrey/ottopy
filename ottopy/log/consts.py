from ottopy.log import Formatter
from ottopy.log.classes import UTCMicroSecFormatter

DEFAULT_SUFFIX = ".log"

FORMATTER = UTCMicroSecFormatter("{asctime} {name} {levelname} >> {message}", style="{")
RAW_FORMATTER = UTCMicroSecFormatter("{asctime} >> {message}", style="{")
# Useful if you're using structlog
PLAIN_FORMATTER = Formatter("{message}", style="{")
