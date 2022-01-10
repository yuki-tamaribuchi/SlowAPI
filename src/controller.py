def sample_controller(request_dict):
	def get(request_dict):
		return 'Hello from sample controller'

class SampleController:
	def get(self):
		return 200, 'Hello from SampleController'

	