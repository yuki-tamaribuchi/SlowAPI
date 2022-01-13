from framework.exception.controller import ControllerResponseDictValidationError

def controller_response_dict_validator(controller_response_dict):
	if ('status_code' and 'custom_headers' and 'body') in controller_response_dict:
		return True
	raise ControllerResponseDictValidationError