from threading import Thread
import datetime

from framework.request.base import load_request
from framework.request.recv import recv_request
from framework.response.generate import generate_response_body_from_file
from framework.response.send import send_response
from framework.http.get import get


class WorkerThread(Thread):
	def __init__(self, client_sock, client_addr):
		self.client_sock = client_sock
		self.client_addr = client_addr


	def request(self):
		request = recv_request(self.client_sock)
		self.request_dict = load_request(request)
		print('{} {} {}'.format(datetime.datetime.now().strftime("%c"), self.client_addr[0], self.request_dict['line']['uri']))


	def response(self):
		if self.request_dict['line']['method']=="GET":
			get(self.client_sock, self.request_dict['line']['uri'])
			
		else:
			send_response(self.client_sock, 501)


	def call(self):
		self.request()
		self.response()


	def start(self):
		self.call()
