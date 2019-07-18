import logging
from logging.config import dictConfig
import time

from justfuckingupdate import __version__

def setup_logging():
	logging.getLogger().name = __name__
	current_time = time.strftime("%Y:%m:%d-%H:%M:%S")
	logging_config = dict(
	version = 1,
	formatters = {
		'f': {'format':
			  '%(name)s %(levelname)-2s %(message)s | %(asctime)s'}
		},
	handlers = {
		'h': {'class': 'logging.StreamHandler',
			  'formatter': 'f',
			  'level': logging.DEBUG}
		},
		root = {
		'handlers': ['h'],
		'level': logging.DEBUG,
		},
)
	dictConfig(logging_config)

def main():
	setup_logging()
	logging.info(f"JustFuckingUpdate - {__version__}.")
