import string
import re

from slowapi.middleware.base import RequestMiddlewareBase
from slowapi.exception.security import HostNotAllowedException
from slowapi.utils.security import remove_special_characters, escape_single_and_double_quote_to_html_entity

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

	exclude_from_special = "&=;\{\}:,_"
	special_chars = re.escape(re.sub("["+exclude_from_special+"]", "", string.punctuation))

	def __call__(self) -> dict:

		sub_path_parameters = {}
		if self.request_dict['path_parameters']:
			for k, v in self.request_dict['path_parameters'].items():
				escaped_v = escape_single_and_double_quote_to_html_entity(v)
				sub_escaped_v = remove_special_characters(escaped_v, self.special_chars)
				sub_path_parameters[k] = sub_escaped_v
			self.request_dict['path_parameters'] = sub_path_parameters

		if self.request_dict['line']['query']:
			escaped_query = escape_single_and_double_quote_to_html_entity(self.request_dict['line']['query'])
			sub_escaped_query = remove_special_characters(escaped_query, self.special_chars)
			self.request_dict['line']['query'] = sub_escaped_query
		
		if self.request_dict['body']:
			escaped_body = escape_single_and_double_quote_to_html_entity(self.request_dict['body'])
			sub_escaped_body = remove_special_characters(escaped_body, self.special_chars)
			self.request_dict['body'] = sub_escaped_body
	
			
		return self.request_dict



		#uri = self.request_dict['line']['uri']
		#special_chars = re.escape(string.punctuation).replace("/", "")
		#escaped_uri = re.sub(r'['+special_chars+r']', "", uri)
		#self.request_dict['line']['uri']=escaped_uri
		#return self.request_dict

