import re

def create_path_parameters_mask(url_patterns):
	path_parameters_masks=[]

	for url_pattern in url_patterns:
		splitted_url_pattern_list = url_pattern['url'].split("/")
		mask = [True if re.match("\<(.*?)\>", token) else False for token in splitted_url_pattern_list]
		path_parameters_masks.append(mask)

	return path_parameters_masks

#パスパラメータのname配列とvalue配列を作成
def extract_path_parameter(url, url_pattern, path_parameters_masks):

	#パスパラメータマスク配列の要素数が1、かつ、その要素がFalseの場合
	#つまり、パスパラメータを使用していない場合
	if len(path_parameters_masks)==1 and path_parameters_masks[0]==False:
		return None, None

	#url_patternを/でスプリット
	splitted_url_pattern = url_pattern['url'].split("/")

	#空の文字列がリストに含まれている場合削除
	if "" in splitted_url_pattern:
		splitted_url_pattern.remove("")

	#urlのスプリット
	splitted_url = url.split("/")

	#上記と同じ
	if "" in splitted_url:
		splitted_url.remove("")

	#パスパラメータが渡されていない場合、空文字を追加
	if len(splitted_url_pattern)-1==len(splitted_url):
		splitted_url.append("")
	#パスパラメータが渡されている場合はそのまま
	elif len(splitted_url_pattern)==len(splitted_url):
		pass
	#それ以外はエラー
	else:
		print("Path parameter name and value error")
	


	#マスクがTrueのところだけ取り出し
	path_parameters_name_arr = [token for mask, token in zip(path_parameters_masks, splitted_url_pattern) if mask]
	path_parameters_value_arr = [token for mask, token in zip(path_parameters_masks, splitted_url) if mask]


	return path_parameters_name_arr, path_parameters_value_arr


#パスパラメータのディクショナリを作成する
#パスパラメータのnameとvalueを受けとって、ディクショナリにして返す
def create_path_parameter_dict(path_parameters_name_arr, path_parameters_value_arr):

	#配列の要素数が同じでなければエラー
	if not (len(path_parameters_name_arr)==len(path_parameters_value_arr)):
		print('Path parameter error')
		return

	path_parameters_dict = {}

	for i in range(len(path_parameters_name_arr)):

		#パラメータのバリューがNoneでなければ回す
		if path_parameters_value_arr[i] is not None:

			#<>を取り除く
			name=path_parameters_name_arr[i][1:-1]

			path_parameters_dict[name]=path_parameters_value_arr[i]

	return path_parameters_dict