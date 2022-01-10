from urls import url_patterns

def dispatcher(request_dict):
	HTTP_METHODS = {
		'GET':'get',
		'POST':'post',
		'PUT':'put',
		'DELETE':'delete'
	}


	def search_url_pattern(url, url_patterns):
		for url_pattern in url_patterns:
			if not url_pattern['url'] == url:
				continue
			elif url_pattern['url'] == url:
				return url_pattern['controller']
			else:
				return

	def is_method_allowed(method):
		if method in HTTP_METHODS:
			return HTTP_METHODS[method]
		return None


	controller_class = search_url_pattern(request_dict['line']['uri'], url_patterns)

	http_method = is_method_allowed(request_dict['line']['method'])

	response_body = ''	

	
	if http_method:
		if controller_class:
			controller_instance = controller_class(request_dict)
			if hasattr(controller_instance, http_method):
				controller_method = getattr(controller_instance, http_method)
				status_code, response_headers, response_body = controller_method()


			else:
				status_code = 405
		else:
			status_code = 404
	else:
		status_code = 501

	response_dict = {
		'line': {
			'status_code': status_code
		},
		'headers':{},
		'body':response_body
	}

	return response_dict