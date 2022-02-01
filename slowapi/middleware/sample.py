from slowapi.middleware.base import ResponseMiddlewareBase, RequestMiddlewareBase


class PrintRequestMiddleware(RequestMiddlewareBase):

	def __call__(self) -> dict:
		print("Request:")
		print(self.request_dict)
		return self.request_dict

class PrintResponseMiddleware(ResponseMiddlewareBase):
	
	def __call__(self):
		print("Response")
		print(self.response_dict)
		return self.response_dict