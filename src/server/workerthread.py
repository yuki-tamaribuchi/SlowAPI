from threading import Thread
import datetime

from request.base import load_request
from request.recv import recv_request
from response.generate import generate_response_body_from_file
from response.send import send_response, response_for_get, response_for_not_implemented_method
from http.get import get


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
			response_for_not_implemented_method(self.client_sock)


	def call(self):
		self.request()
		self.response()


	def start(self):
		self.call()
