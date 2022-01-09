from response.generate import generate_http_response_line

def send_msg(client_sock, msg):
		client_sock.send(bytes(msg, 'utf-8'))


def send_response(client_sock, msg):
	send_msg(client_sock, msg)


def response_for_get(client_sock):
		send_response(client_sock, generate_http_response_line(200))
		send_response(client_sock, '\r\n')

def response_for_not_implemented_method(client_sock):
	send_response(client_sock, 'HTTP/1.1 501 Not Implemented\r\n')