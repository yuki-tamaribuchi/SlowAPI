from slowapi.controller.executer import execute


def dispatch(request_dict):
	return execute(request_dict)

