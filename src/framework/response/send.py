from framework.response.generate import generate_http_response_line

def send_msg(client_sock, msg):
		client_sock.send(bytes(msg, 'utf-8'))


def send_response(client_sock, status_code, response=None):
	send_msg(client_sock, generate_http_response_line(status_code))
	if response:
		send_msg(client_sock, response)