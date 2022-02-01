import re
import string

def remove_special_characters(input_string, special_chars=None):
	if special_chars is None:
		special_chars = re.escape(string.punctuation)
	
	return re.sub(r'['+special_chars+r']', "", input_string)


def escape_single_quote_to_html_entity(input_string):
	return input_string.replace("'", "&#39;")

def escape_double_quote_to_html_entity(input_string):
	return input_string.replace("\"", "&quot;")

def escape_single_and_double_quote_to_html_entity(input_string):
	return escape_single_quote_to_html_entity(
		escape_double_quote_to_html_entity(
			input_string
		)
	)