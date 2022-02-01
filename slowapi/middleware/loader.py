from slowapi.middleware.base import RequestMiddlewareBase, ResponseMiddlewareBase
from slowapi.exception.middleware import MiddlewareNotInheritancedException


def load_custom_middlewares(request_dict):
	custom_middlewares = request_dict['url_pattern']['middlewares']
	return custom_middlewares


def append_middleware_to_request_dict(request_dict, request_middlewares, response_middlewares):
		request_dict['middlewares'] = {}
		request_dict['middlewares']['request'] = request_middlewares
		request_dict['middlewares']['response'] = response_middlewares
		return request_dict



def load(request_dict, default_middlewares):
	custom_middlewares = load_custom_middlewares(request_dict)

	middlewares = default_middlewares+custom_middlewares

	request_middlewares = []
	response_middlewares = []

	for middleware in middlewares:
		if issubclass(middleware, RequestMiddlewareBase) and issubclass(middleware, ResponseMiddlewareBase):
			request_middlewares.append(middleware)
			response_middlewares.append(middleware)

		elif issubclass(middleware, RequestMiddlewareBase):
			request_middlewares.append(middleware)

		elif issubclass(middleware, ResponseMiddlewareBase):
			response_middlewares.append(middleware)

		else:
			raise MiddlewareNotInheritancedException(middleware)

	request_dict = append_middleware_to_request_dict(request_dict, request_middlewares, response_middlewares)
	
	return request_dict