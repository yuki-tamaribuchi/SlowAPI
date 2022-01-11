import datetime
import re

from framework.response.generate import generate_response_headers

from urls import url_patterns

def dispatcher(request_dict):
	HTTP_METHODS = {
		'GET':'get',
		'POST':'post',
		'PUT':'put',
		'DELETE':'delete'
	}

	def create_path_parameters_mask(url_patterns):
		path_parameters_masks=[]
		for url_pattern in url_patterns:
			splitted_url_pattern_list = url_pattern['url'].split("/")
			mask = [True if re.match("\<(.*?)\>", token) else False for token in splitted_url_pattern_list]
			path_parameters_masks.append(mask)
		return path_parameters_masks


	def is_matched_path(url, url_pattern, path_parameters_mask):
		path_mask = [False if element else True for element in path_parameters_mask]
		splitted_url = url.split("/")
		if "" in splitted_url:
			splitted_url.remove("")

		splitted_url_pattern = url_pattern['url'].split("/")
		if "" in splitted_url_pattern:
			splitted_url_pattern.remove("")

		masked_url = [token for mask, token in zip(path_mask, splitted_url) if mask]
		masked_url_pattern = [token for mask, token in zip(path_mask, splitted_url_pattern) if mask]
		if masked_url == masked_url_pattern:
			return True
		return False
		

	
	def path_matching(url, url_patterns, path_parameters_masks):
		matched_idx = []
		for i in range(len(url_patterns)):
			if is_matched_path(url, url_patterns[i], path_parameters_masks[i]):
				matched_idx.append(i)
		if len(matched_idx)==1:
			return matched_idx[0]
		elif not len(matched_idx)==1:
			print('Path matching error')
			return
		return

	


	def extract_path_parameter(url, url_pattern, path_parameters_mask):
		splitted_url_pattern = url_pattern['url'].split("/")
		if "" in splitted_url_pattern:
			splitted_url_pattern.remove("")

		splitted_url = url.split("/")
		if "" in splitted_url:
			splitted_url.remove("")
		
		path_parameters_name = [token for mask, token in zip(path_parameters_mask, splitted_url_pattern) if mask]
		path_parameters_value = [token for mask, token in zip(path_parameters_mask, splitted_url) if mask]
		return path_parameters_name, path_parameters_value



	def create_path_parameter_dict(path_parameters_name, path_parameters_value):
		if not (len(path_parameters_name)==len(path_parameters_value)):
			print('Path parameter error')
			return
		path_parameters_dict = {}
		for i in range(len(path_parameters_name)):
			if path_parameters_value[i]:
				name=path_parameters_name[i][1:-1]
				path_parameters_dict[name]=path_parameters_value[i]
		return path_parameters_dict

		

	def search_url_pattern(url, url_patterns):
		path_parameters_masks = create_path_parameters_mask(url_patterns)
		matched_idx = path_matching(url, url_patterns, path_parameters_masks)
		if matched_idx:
			path_parameters_name, path_parameters_value = extract_path_parameter(url, url_patterns[matched_idx], path_parameters_masks[matched_idx])
			path_parameters_dict = create_path_parameter_dict(path_parameters_name, path_parameters_value)
			return url_patterns[matched_idx]['controller'], path_parameters_dict
		return



	def is_method_allowed(method):
		if method in HTTP_METHODS:
			return HTTP_METHODS[method]
		return None


	controller_class, path_parameters_dict = search_url_pattern(request_dict['line']['uri'], url_patterns)
	request_dict['path_parameters'] = path_parameters_dict

	http_method = is_method_allowed(request_dict['line']['method'])

	response_body = ''	
	custom_headers = {}
	
	if http_method:
		if controller_class:
			controller_instance = controller_class(request_dict)
			if hasattr(controller_instance, http_method):
				controller_method = getattr(controller_instance, http_method)
				status_code, custom_headers, response_body = controller_method()


			else:
				status_code = 405
		else:
			status_code = 404
	else:
		status_code = 501


	headers = {
		'Connection': 'Keep-Alive',
		'Content-Type': 'application/json',
		'Date': datetime.datetime.now().strftime("%a, %d %b %Y %X %Z"),
		'Keep-Alive':'timeout=5'
	}

	headers.update(custom_headers)
	response_headers = generate_response_headers(headers)

	
	response_dict = {
		'line': {
			'status_code': status_code
		},
		'headers':response_headers,
		'body':response_body
	}

	return response_dict