import re

def extract_emails(text):
	pattern = r'[a-z0-9._%+-]+@[a-z0-9.-]+\.com'
	return re.findall(pattern, text)