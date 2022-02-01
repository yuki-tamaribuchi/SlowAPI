class URLResolveNotFoundException(Exception):
	def __init__(self, url):
		print('{} was not resolved'.format(url))