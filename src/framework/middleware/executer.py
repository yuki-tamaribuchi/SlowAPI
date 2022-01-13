def execute_request_middlewares(request_dict):
		for middleware in request_dict['middlewares']['request']:
			request_dict = middleware(request_dict)()
		return request_dict


def execute_response_middlewares(request_dict, response_dict):
		middlewares = request_dict['middlewares']['response']
		if middlewares:
			for middleware in middlewares:
				response_dict = middleware(response_dict)()
			return response_dict
		return response_dict