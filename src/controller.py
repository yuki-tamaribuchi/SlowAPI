def sample_controller(request_dict):
	def get(request_dict):
		return 'Hello from sample controller'

class SampleController:
	def __init__(self, request_dict):
		self.request_dict = request_dict

	def get(self):
		return 200, 'Hello from SampleController Get'
	