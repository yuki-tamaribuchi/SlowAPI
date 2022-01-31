class HostNotAllowedException(Exception):
	def __init__(self, host):
		print('{} is not allowed host'.format(host))