import re

def parse_review(full_review):
	''' Process text content of a NY Times review. Removes the header and
		footer (cast) sections. Also converts to lower case, removes punctuation
		and tokenizes the remaining string.

	@full_review: The string containing the full review text.
	'''
	review_body = remove_nytimes_review_header(full_review)		# Remove NYTimes review header
	review_body = remove_nytimes_review_footer(review_body)
	review_body = remove_punctuation(review_body)
	review_body = review_body.lower()
	text_itemset = review_body.split() 							# Split the review on spaces into tokens

	return text_itemset


def remove_nytimes_review_header(text):
	''' Function which uses a regular expression to remove the header content
		from an NY Times movie review.

	@text: The text content of the review.
	'''
	regex = r"\A(\n{2})((.+\n{1,2})*\n)"						# Regex matching NY Times review header
	match = re.match(regex, text)

	return text[match.end():]


def remove_nytimes_review_footer(text):
	''' Function which uses a regular expression to remove the footer (cast)
		content from the end of a movie review (if it is present).

	@text: The text content of the review.
	'''
	regex = r"\n{2,}(.+\n)*(.*(\s\.){1,}.*\n)+(.+\n{1,})*(\n*)\Z"		# Regex matching NY Times review footer
	match = re.search(regex, text)

	if match is None:
		return text
	else:
		return text[:match.start()]


def remove_punctuation(text):
	''' Function that removes punctuation from the review text.

	@text: The text content of the review.
	'''
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