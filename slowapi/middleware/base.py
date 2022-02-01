from abc import abstractmethod, ABCMeta

class RequestMiddlewareAbstractClass(object):
	__metaclass__ = ABCMeta

	@abstractmethod
	def __call__(self) -> dict:
		raise NotImplementedError


class RequestMiddlewareBase(RequestMiddlewareAbstractClass):
	def __init__(self, request_dict):
		self.request_dict = request_dict


class ResponseMiddlewareAbstractClass(object):
	__metaclass__ = ABCMeta

	@abstractmethod
	def __call__(self):
		raise NotImplementedError


class ResponseMiddlewareBase(ResponseMiddlewareAbstractClass):
	def __init__(self, response_dict):
		self.response_dict = response_dict