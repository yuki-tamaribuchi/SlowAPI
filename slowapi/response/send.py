from framework.response.generate import generate_http_response_line

def send_msg(client_sock, msg):
		if not msg == "" or not None:
			client_sock.send(bytes(msg, 'utf-8'))


def send_response(client_sock, response_dict):
	send_msg(client_sock, generate_http_response_line(response_dict['line']['status_code']))
	send_msg(client_sock, response_dict['headers'])
	send_msg(client_sock, '\r\n')
	send_msg(client_sock, response_dict['body'])
	send_msg(client_sock, '\r\n')


	#send_msg(client_sock, generate_http_response_line(status_code))
	#if response:
	#	send_msg(client_sock, response)
	#	send_msg(client_sock, "\r\n")