import datetime

from framework.response.generate import generate_response_dict, generate_response_headers
from framework.controller.validator import controller_response_dict_validator
from framework.http.methods import is_method_allowed



def call_controller(controller_method):
	controller_response_dict = controller_method()
	if controller_response_dict_validator(controller_response_dict):
		return controller_response_dict

def extract_controller_response_dict(controller_response_dict):
	return controller_response_dict['status_code'], controller_response_dict['custom_headers'], controller_response_dict['body']

def merge_headers(default_headers, custom_headers):
	default_headers.update(custom_headers)
	return default_headers



def execute(request_dict):
	headers = {
		'Content-Type': 'application/json',
		'Date': datetime.datetime.now().strftime("%a, %d %b %Y %X %Z"),
	}

	status_code = 500
	custom_headers = {}
	response_body = ''	
	

	http_method = is_method_allowed(request_dict['line']['method'])

	if http_method:
		controller_class = request_dict['url_pattern']['controller']
	
		if controller_class:
			controller_instance = controller_class(request_dict)

			#コントローラインスタンスに、呼び出されたHTTPメソッドに対応するメソッドがあるか確認
			if hasattr(controller_instance, http_method):

				#HTTPメソッドに対応するメソッドを取得
				controller_method = getattr(controller_instance, http_method)

				controller_response_dict = call_controller(controller_method)

				status_code, custom_headers, response_body = extract_controller_response_dict(controller_response_dict)

				headers = merge_headers(headers, custom_headers)

			else:
				#メソッドが実装されていない場合の処理
				#でも、先にNotImplementedErrorがraiseして呼び出されないかも
				status_code = 405
		else:
			#コントローラクラスが登録されていない場合
			#400 Bad Request
			status_code = 400
	else:
		#対応していないHTTPメソッドが呼び出された場合
		#現在は、GET, POST, PUT, DELETEのみ対応
		#それ以外は私がまだ使い方がわかっていないので未実装
		#一応今後実装する予定
		#501 Not Implemented
		status_code = 501


	response_headers = generate_response_headers(headers)
	response_dict = generate_response_dict(
		status_code=status_code,
		headers=response_headers,
		body=response_body
	)

	return response_dict