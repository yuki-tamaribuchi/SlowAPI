from framework.server.server import Server
from settings import *
from settings.server import SERVER_LISTEN_IP_ADDR, SERVER_LISTEN_PORT

try:
	server = Server(SERVER_LISTEN_IP_ADDR, SERVER_LISTEN_PORT)
	server.serve()
except KeyboardInterrupt:
	pass