from ottopy.log.classes import UTCMicroSecFormatter

DEFAULT_SUFFIX = ".log"

FORMATTER = UTCMicroSecFormatter("{asctime} {name} {levelname} >> {message}", style="{")
RAW_FORMATTER = UTCMicroSecFormatter("{asctime} >> {message}", style="{")
