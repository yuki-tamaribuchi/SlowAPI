import datetime
import re

from framework.response.generate import generate_response_headers
from framework.middleware.base import RequestMiddlewareBase, ResponseMiddlewareBase
from framework.exception.middleware import MiddlewareNotInheritancedException

from urls import url_patterns
from settings.middleware import MIDDLEWARES

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
			return True, len(masked_url)
		return False, None
		

	
	def path_matching(url, url_patterns, path_parameters_masks):
		matched_idx_arr = []
		matched_length_arr = []
		for i in range(len(url_patterns)):
			is_matched, matched_length = is_matched_path(url, url_patterns[i], path_parameters_masks[i])
			if is_matched:
				matched_idx_arr.append(i)
				matched_length_arr.append(matched_length)

		if len(matched_idx_arr)==1:
			return matched_idx_arr[0]

		elif not len(matched_idx_arr)==1:
			#もし2つ以上マッチしていたら最長一致法で選択する
			max_length_idx = matched_idx_arr[matched_length_arr.index(max(matched_length_arr))]

			#しかし、もしmatched_length_arrに同値が入っていたらどうするか決めていない
			#この場合前方からサーチして最初に見つかったインデックスになる

			
			return max_length_idx
			



	def extract_path_parameter(url, url_pattern, path_parameters_mask):
		if len(path_parameters_mask)==1 and path_parameters_mask[0]==False:
			return None, None

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
		path_parameters_dict = {}
		path_parameters_masks = create_path_parameters_mask(url_patterns)
		matched_idx = path_matching(url, url_patterns, path_parameters_masks)
		if not matched_idx is None:
			path_parameters_name, path_parameters_value = extract_path_parameter(url, url_patterns[matched_idx], path_parameters_masks[matched_idx])
			if path_parameters_name and path_parameters_value:
				path_parameters_dict = create_path_parameter_dict(path_parameters_name, path_parameters_value)

			return url_patterns[matched_idx]['controller'], path_parameters_dict, url_patterns[matched_idx]['middlewares']
		return



	def is_method_allowed(method):
		if method in HTTP_METHODS:
			return HTTP_METHODS[method]
		return None



	def load_middlewares(default_middlewares, custom_middlewares):
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

		return request_middlewares, response_middlewares



	
	def append_middleware_to_request_dict(request_dict, request_middlewares, response_middlewares):
		request_dict['middlewares'] = {}
		request_dict['middlewares']['request'] = request_middlewares
		request_dict['middlewares']['response'] = response_middlewares
		return request_dict





	controller_class, path_parameters_dict, middlewares = search_url_pattern(request_dict['line']['uri'], url_patterns)

	request_dict['path_parameters'] = path_parameters_dict






	request_middlewares, response_middlewares = load_middlewares(MIDDLEWARES, middlewares)
	request_dict = append_middleware_to_request_dict(request_dict, request_middlewares, response_middlewares)
	


	def execute_request_middlewares(request_dict):
		for middleware in request_dict['middlewares']['request']:
			request_dict = middleware(request_dict)()
		return request_dict

	request_dict = execute_request_middlewares(request_dict)







	

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



	def execute_response_middlewares(request_dict, response_dict):
		middlewares = request_dict['middlewares']['response']
		if middlewares:
			for middleware in middlewares:
				response_dict = middleware(response_dict)()
			return response_dict
		return response_dict

	response_dict = execute_response_middlewares(request_dict, response_dict)




	return response_dict