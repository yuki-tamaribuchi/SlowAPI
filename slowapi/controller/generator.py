def generate_controller_response_dict(status_code:int, custom_headers:dict, body:str):
	controller_response_dict = {
		'status_code': status_code,
		'custom_headers': custom_headers,
		'body': body
	}

	return controller_response_dict