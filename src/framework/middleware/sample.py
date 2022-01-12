from framework.middleware.base import ResponseMiddlewareBase

class SampleResponseMiddleware(ResponseMiddlewareBase):
	
	def __call__(self):
		print(self.response_dict)
		return self.response_dict