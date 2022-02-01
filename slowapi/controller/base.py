from abc import ABCMeta, abstractmethod


class ControllerAbstractClass:
	__metaclass__ = ABCMeta

	@abstractmethod
	def get(self) -> dict:
		raise NotImplementedError

	@abstractmethod
	def post(self) -> dict:
		raise NotImplementedError

	@abstractmethod
	def put(self) -> dict:
		raise NotImplementedError

	@abstractmethod
	def delete(self) -> dict:
		raise NotImplementedError


class ControllerBase(ControllerAbstractClass):
	def __init__(self, request_dict:dict) -> None:
		self.request_dict = request_dict
