# Imports
import logging
import logging.config
import os.path

# Create logging configuration
def log_config():
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            },
        },
        "handlers": {
            "default_handler": {
                "class": "logging.FileHandler",
                "level": "DEBUG",
                "formatter": "standard",
                "filename": "/mnt/d/Documents/Data Projects/formula_1_racing/loggers/ergast_etl_pipeline.log",
                "encoding": "utf8"
            },
        },
        "loggers": {
            "": {
                "handlers": ["default_handler"],
                "level": "DEBUG",
                "propagate": False
            }
        }
    }
    logging.config.dictConfig(config)

if __name__ == "__main__":
    log_config()
