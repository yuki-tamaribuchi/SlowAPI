class MiddlewareNotInheritancedException(Exception):
	def __init__(self, middleware):
		print('{} is not inheritanced base class'.format(middleware.__class__.__name__))