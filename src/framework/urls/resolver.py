from framework.urls.parameter import create_path_parameters_mask, extract_path_parameter, create_path_parameter_dict
from framework.exception.urls import URLResolveNotFoundExecption


def is_matched_path(url, url_pattern, path_parameters_mask):
	path_mask = [False if element else True for element in path_parameters_mask]
	splitted_url = url.split("/")

	if "" in splitted_url:
		splitted_url.remove("")

	splitted_url_pattern = url_pattern['url'].split("/")

	if "" in splitted_url_pattern:
		splitted_url_pattern.remove("")

	masked_url = [token for mask, token in zip(path_mask, splitted_url) if mask]
	masked_url_pattern = [token for mask, token in zip(path_mask, splitted_url_pattern) if mask]

	if masked_url == masked_url_pattern:
		return True, len(masked_url)

	return False, None



def path_matching(url, url_patterns, path_parameters_masks):
	matched_idx_arr = []
	matched_length_arr = []

	for i in range(len(url_patterns)):
		is_matched, matched_length = is_matched_path(url, url_patterns[i], path_parameters_masks[i])

		if is_matched:
			matched_idx_arr.append(i)
			matched_length_arr.append(matched_length)

	if len(matched_idx_arr)==1:
		return matched_idx_arr[0]

	elif  len(matched_idx_arr)>1:

		#もし2つ以上マッチしていたら最長一致法で選択する
		max_length_idx = matched_idx_arr[matched_length_arr.index(max(matched_length_arr))]
		#しかし、もしmatched_length_arrに同値が入っていたらどうするか決めていない
		#この場合前方からサーチして最初に見つかったインデックスになる

		return max_length_idx
	
	return



def resolve(request_dict, url_patterns):
	path_parameters_dict = {}

	url = request_dict['line']['uri']
	
	#パスパラメータをしていしている所(<>で括っている所)をTrueで、それ以外をFalseでマスクを作成
	path_parameters_masks = create_path_parameters_mask(url_patterns)

	#マッチしたurl_patternのインデックスを取得
	matched_idx = path_matching(url, url_patterns, path_parameters_masks)

	if matched_idx is None:
		raise URLResolveNotFoundExecption(url)


	path_parameters_name, path_parameters_value = extract_path_parameter(url, url_patterns[matched_idx], path_parameters_masks[matched_idx])
	if path_parameters_name and path_parameters_value:
		path_parameters_dict = create_path_parameter_dict(path_parameters_name, path_parameters_value)

	request_dict['url_pattern'] = url_patterns[matched_idx]
	request_dict['path_parameters'] = path_parameters_dict

	return request_dict