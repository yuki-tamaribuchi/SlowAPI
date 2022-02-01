from framework.response.generate import generate_response_body_from_file
from framework.response.send import send_response

def get(client_sock, filepath):
	send_response(client_sock, 200, generate_response_body_from_file(filepath))