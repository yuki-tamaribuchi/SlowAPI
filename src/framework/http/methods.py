HTTP_METHODS = {
	'GET':'get',
	'POST':'post',
	'PUT':'put',
	'DELETE':'delete'
}

def is_method_allowed(method):
	if method in HTTP_METHODS:
		return HTTP_METHODS[method]
	return None