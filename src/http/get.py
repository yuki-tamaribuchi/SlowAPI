from response.generate import generate_response_body_from_file
from response.send import response_for_get, send_response, send_msg

def get(client_sock, filepath):
	response_for_get(client_sock)
	send_response(client_sock, generate_response_body_from_file(filepath))