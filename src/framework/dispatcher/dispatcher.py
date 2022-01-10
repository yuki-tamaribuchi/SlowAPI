from urls import url_patterns

def dispatcher(request_dict):
	def search_url_pattern(url, url_patterns):
		for url_pattern in url_patterns:
			if not url_pattern['url'] == url:
				continue
			elif url_pattern['url'] == url:
				return url_pattern['controller']
			else:
				return


	controller_class = search_url_pattern(request_dict['line']['uri'], url_patterns)

	response_body = ''	

	

	if controller_class:
		controller_instance = controller_class()
		if hasattr(controller_class, 'get'):
			status_code = 200
			response_body = controller_instance.get()
		else:
			status_code = 501
			response_body = ''
	else:
		status_code = 404

	response_dict = {
		'line': {
			'status_code': status_code
		},
		'body':response_body
	}

	return response_dict