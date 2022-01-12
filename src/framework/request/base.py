def load_request(request):
	def split_request_line_and_other(request):
		return request.split("\r\n", 1)

	def split_request_line(request_line):
		return request_line.split(" ", 2)

	def split_request_uri_and_query(request_uri_and_query):
		if "?" in request_uri_and_query:
			return request_uri_and_query.split("?")
		return request_uri_and_query, ""

	def split_request_header_and_body(request_header_and_body):
		request_header_and_body_list = request_header_and_body.split("\r\n")
		return request_header_and_body_list[:-1], request_header_and_body_list[-1]

	def create_headers_dict(header):
		headers = {}
		for line in header:
			name, data = line.split(":", 1)
			headers[name] = data[1:]
		return headers
	
	request = request.decode('utf-8')
	request_line, request_header_and_body = split_request_line_and_other(request)
	request_method, request_uri_and_query, request_http_proto = split_request_line(request_line)
	request_uri, request_query = split_request_uri_and_query(request_uri_and_query)
	request_header, request_body = split_request_header_and_body(request_header_and_body)
	request_headers = create_headers_dict(request_header[:-1])


	request_dict = {
		'line':{
			'method': request_method,
			'uri': request_uri[1:],
			'query': request_query,
			'http_proto':request_http_proto,
		},
		'headers': request_headers,
		'body': request_body
	}

	return request_dict