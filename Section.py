#Section class
class Section:
	crn_code = ''
	subject_code = ''
	class_number = ''
	cle_code = ''
	term_year = ''
	open_only = ''

	def __init__(self, crn_code, subject_code, class_number, cle_code, term_year, open_only):
		self.crn_code = crn_code
		self.subject_code = subject_code
		self.class_number = class_number
		self.cle_code = cle_code
		self.term_year = term_year
		self.open_only = open_only

	def __str__(self):
		return getattr(self, 'crn_code') + ' ' + getattr(self, 'subject_code') + '-' + getattr(self, 'class_number')