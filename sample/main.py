import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import logging
import logging.config
from os import path

from slowapi.server.server import Server
from settings import *
from settings.server import SERVER_LISTEN_IP_ADDR, SERVER_LISTEN_PORT

logging_config_filepath = path.join(path.dirname(path.abspath(__file__)), "logging.conf")
logging.config.fileConfig(logging_config_filepath, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

try:
	server = Server(SERVER_LISTEN_IP_ADDR, SERVER_LISTEN_PORT)
	server.serve()
except Exception as e:
	logger.exception(e)
except KeyboardInterrupt:
	pass