import socket

from server.workerthread import WorkerThread

class Server:

	def serve(self):
		

		try:
			sock = socket.socket(
				family=socket.AF_INET,
				type=socket.SOCK_STREAM
			)
			sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

			sock.bind(('127.0.0.1', 8000))

			sock.listen(5)

			while True:
				client_sock, client_addr = sock.accept()

				thread = WorkerThread(client_sock, client_addr)
				thread.start()

				client_sock.close()
		finally:
			sock.close()