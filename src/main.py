from server.server import Server
from settings import *

try:
	
	server = Server()

	print('Server was started at 127.0.0.1:8000')
	server.serve()
finally:
	print('Server was stopped...')