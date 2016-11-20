import re
import string

def parse_review(full_review):
	review_body = remove_nytimes_review_header(full_review)		# Remove NYTimes review header
	review_body = remove_nytimes_review_footer(review_body)
	review_body = remove_punctuation(review_body)
	review_body = review_body.lower()
	text_itemset = review_body.split() 							# Split the review on spaces into tokens

	return text_itemset

def remove_nytimes_review_header(text):
	regex = r"\A(\n{2})((.+\n{1,2})*\n)"						# Regex matching NY Times review header
	match = re.match(regex, text)

	return text[match.end():]

def remove_nytimes_review_footer(text):
	regex = r"\n\n(.+\n)*(.*(\s\.){1,}.*\n)+(.+\n)*\Z"			# Regex matching NY Times review footer
	match = re.search(regex, text)

	if match is None:
		return text
	else:
		return text[:match.start()]

def remove_punctuation(text):
	text = text.replace(',', "")
	text = text.replace('"', "")
	text = text.replace('.', "")
	text = text.replace('...', "")
	text = text.replace('?', "")
	text = text.replace('!', "")
	text = text.replace(';', "")
	text = text.replace('(', "")
	text = text.replace(')', "")
	text = text.replace(':', "")
	text = text.replace(u'\u2014', " ")	# Emdash
	return text