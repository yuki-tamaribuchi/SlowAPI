import string
import re

from framework.middleware.base import RequestMiddlewareBase
from framework.exception.security import HostNotAllowedException

from settings.hosts import HOSTS

class AllowedHostMiddleware(RequestMiddlewareBase):

	def __call__(self) -> dict:
		if "*" in HOSTS:
			return self.request_dict

		host = self.request_dict['headers']['Host']

		if ":" in host:
			host = host.split(":")[0]

		if host in HOSTS:
			return self.request_dict
		
		raise HostNotAllowedException(host)


class SQLInjectionProtectMiddleware(RequestMiddlewareBase):

	def __call__(self) -> dict:
		special_chars = re.escape(string.punctuation).replace("/", "")
		sub_path_parameters = {}
		if self.request_dict['path_parameters']:
			for k, v in self.request_dict['path_parameters'].items():
				sub_v = re.sub(r'['+special_chars+r']', "", v)
				sub_path_parameters[k] = sub_v
			self.request_dict['path_parameters'] = sub_path_parameters
		return self.request_dict



		#uri = self.request_dict['line']['uri']
		#special_chars = re.escape(string.punctuation).replace("/", "")
		#escaped_uri = re.sub(r'['+special_chars+r']', "", uri)
		#self.request_dict['line']['uri']=escaped_uri
		#return self.request_dict

