import logging

suppress_commands = False

class CommandFilter(logging.Filter):
    def filter(self, record):
        if suppress_commands and record.name.startswith("cli.commands"):
            return False
        return True

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)     # global level

    # Console (for user)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)     # user sees only INFO
    console.setFormatter(logging.Formatter("%(message)s"))
    console.addFilter(CommandFilter())

    # File (dev debugging)
    filelog = logging.FileHandler("friendnet.log")
    filelog.setLevel(logging.DEBUG)    # dev sees everything
    filelog.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    ))
    #filelog.addFilter(CommandFilter()) # Uncomment to prevent command logs from hitting the log file

    logger.addHandler(console)
    logger.addHandler(filelog)


