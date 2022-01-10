def generate_http_response_line(status_code):
		HTTP_STATUS_CODE = {
			200:'200 OK',
			404:'404 Not Found',
			405:'405 Method Not Allowed',
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
