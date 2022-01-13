def generate_http_response_line(status_code):
		HTTP_STATUS_CODE = {
			200:'200 OK',
			400:'400 Bad Request',
			404:'404 Not Found',
			405:'405 Method Not Allowed',
			500:'500 Internal Server Error',
			501:'501 Not Implemented'
		}

		return 'HTTP/1.1 {}\r\n'.format(HTTP_STATUS_CODE[status_code])


def generate_response_body_from_file(filepath):
		try:
			with open("static/"+filepath, 'r') as f:
				body = f.read()
			return body
		except (FileNotFoundError, IsADirectoryError) as e:
			return ''


def generate_response_headers(headers_dict):
	headers = ""
	
	for k, v in headers_dict.items():
		header = '{}: {}\r\n'.format(k, v)
		headers+=header
	
	return headers


def generate_response_dict(status_code, headers, body):
	response_dict = {
		'line':{
			'status_code':status_code
		},
		'headers':headers,
		'body':body
	}
	return response_dict