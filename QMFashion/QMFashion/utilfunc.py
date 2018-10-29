def extract_first_paragraph(response, first_para_extractor):
	child_int = 1
	while True:
		first_para_text = "" + first_para_extractor + " p:nth-of-type("+ str(child_int) + ") *::text"
		first_paragraph = ''.join(response.css(first_para_text).extract())
		if len(first_paragraph) > 13:
			return first_paragraph
		child_int = child_int + 1
		if child_int > 10:
			return None