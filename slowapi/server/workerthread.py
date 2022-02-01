from threading import Thread
import datetime

from slowapi.request.base import load_request
from slowapi.request.recv import recv_request
from slowapi.response.generate import generate_response_dict
from slowapi.response.send import send_response
from slowapi.http.get import get
from slowapi.dispatcher.dispatcher import dispatch
from slowapi.urls.resolver import resolve
from slowapi.middleware.loader import load as load_middlewares
from slowapi.middleware.executer import execute_request_middlewares, execute_response_middlewares
from slowapi.exception.security import HostNotAllowedException
from slowapi.exception.urls import URLResolveNotFoundException

from urls import url_patterns
from settings.middleware import MIDDLEWARES


class WorkerThread(Thread):
	def __init__(self, client_sock, client_addr):
		self.client_sock = client_sock
		self.client_addr = client_addr
		self.request_dict = {}
		self.response_dict = {}


	def recv_and_load_request(self):
		request = recv_request(self.client_sock)
		self.request_dict = load_request(request)
		print('{} {} {} {}'.format(datetime.datetime.now().strftime("%c"), self.client_addr[0], self.request_dict['line']['method'], self.request_dict['line']['uri']))

	def url_resolve(self):
		self.request_dict = resolve(self.request_dict, url_patterns)

	def load_middleware(self):
		self.request_dict = load_middlewares(self.request_dict, MIDDLEWARES)

	def exc_request_middleware(self):
		self.request_dict = execute_request_middlewares(self.request_dict)

	def dispatch_request(self):
		self.response_dict=dispatch(self.request_dict)

	def exc_response_middleware(self):
		self.response_dict = execute_response_middlewares(self.request_dict, self.response_dict)

	def response(self):
		send_response(self.client_sock, self.response_dict)


	def call(self):
		try:
			self.recv_and_load_request()
			self.url_resolve()
			self.load_middleware()
			self.exc_request_middleware()
			self.dispatch_request()
			self.exc_response_middleware()
		except HostNotAllowedException as e:
			self.response_dict = generate_response_dict(400, "", "Host Not Allowed: {}".format(e.args[0]))
		except URLResolveNotFoundException:
			self.response_dict = generate_response_dict(404, "", "URL Not Found")
		finally:
			self.response()
		


	def start(self):
		self.call()
