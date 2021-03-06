import socket

from slowapi.server.workerthread import WorkerThread

class Server:
	def __init__(self, ip_addr, port):
		self.ip_addr = ip_addr
		self.port = port

	def serve(self):
		

		print('Server was started at http://{}:{}\nTo stop server, press ctrl+c'.format(self.ip_addr, self.port))
		sock = socket.socket(
			family=socket.AF_INET,
			type=socket.SOCK_STREAM
		)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		sock.bind((self.ip_addr, self.port))

		sock.listen(5)

		while True:
			client_sock, client_addr = sock.accept()

			thread = WorkerThread(client_sock, client_addr)
			thread.start()

			client_sock.close()
