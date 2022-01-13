import re

def create_path_parameters_mask(url_patterns):
	path_parameters_masks=[]

	for url_pattern in url_patterns:
		splitted_url_pattern_list = url_pattern['url'].split("/")
		mask = [True if re.match("\<(.*?)\>", token) else False for token in splitted_url_pattern_list]
		path_parameters_masks.append(mask)

	return path_parameters_masks


def extract_path_parameter(url, url_pattern, path_parameters_mask):
	if len(path_parameters_mask)==1 and path_parameters_mask[0]==False:
		return None, None

	splitted_url_pattern = url_pattern['url'].split("/")

	if "" in splitted_url_pattern:
		splitted_url_pattern.remove("")

	splitted_url = url.split("/")

	if "" in splitted_url:
		splitted_url.remove("")
	
	path_parameters_name = [token for mask, token in zip(path_parameters_mask, splitted_url_pattern) if mask]
	path_parameters_value = [token for mask, token in zip(path_parameters_mask, splitted_url) if mask]

	return path_parameters_name, path_parameters_value



def create_path_parameter_dict(path_parameters_name, path_parameters_value):
	if not (len(path_parameters_name)==len(path_parameters_value)):
		print('Path parameter error')
		return

	path_parameters_dict = {}

	for i in range(len(path_parameters_name)):
		if path_parameters_value[i]:
			name=path_parameters_name[i][1:-1]
			path_parameters_dict[name]=path_parameters_value[i]

	return path_parameters_dict