from pyvt import Timetable
import webbrowser
import time
import os
import sys

# Usage information
if  len(sys.argv) >= 1 and (sys.argv[1] == '-help' or sys.argv[1] == '-h'
		or sys.argv[1] == '--help' or sys.argv[1] == '--h'):
	print("Usage: -d <input directory> <output directory>\n\t-d Specify delay for checking course availabilities (in seconds)\n\t"
		+ "<input directory> The directory of the .txt file with courses to check availabilities\n\t<output directory The directory"
		+ " of the .txt file with availability information")
	sys.exit()

# Determines intervals for checking section availability (units in seconds)
delay = 10;
if len(sys.argv) >= 2:
	delay = int(sys.argv[1])
# File containing sections to listen to
input_file_name = 'listening_list.txt';
if len(sys.argv) >= 3:
	input_file_name = sys.argv[2]
# File containing available sections
output_file_name = 'available_sections.txt';
if len(sys.argv) >= 4:
	output_file_name = sys.argv[3]

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

#List of actively listening courses
sections = []

#Read section list via input file
with open(input_file_name) as inputFile:
	for line in inputFile:
		parts = line.split('|')
		if len(parts) != 6:
			continue
		#print(parts)
		parts[5] = parts[5].strip('\n')
		section = Section(parts[0], parts[1], parts[2], parts[3], parts[4], parts[5]);
		if len(getattr(section, 'crn_code')) < 6:
			setattr(section, 'crn_code', '')
		sections.append(section)

timetable = Timetable()
# Allow loop if listening to classes
if (len(sections) > 0):
	while (True):
		output_file = open(output_file_name, 'w')
		for section in sections:
			available_sections = []
			# Lookup section by crn if available
			if getattr(section, 'crn_code'):
				#print('lookup via crn [' + str(len(getattr(section, 'crn_code'))) + ']')
				#print(str(getattr(section, 'crn_code')));
				available_sections = timetable.crn_lookup(getattr(section, 'crn_code'), getattr(section, 'term_year'), getattr(section, 'open_only'))
			# Lookup section by subject code and clas number
			elif getattr(section, 'subject_code') and getattr(section, 'class_number'):
				#print('lookup via class')
				available_sections = timetable.class_lookup(getattr(section, 'subject_code'), getattr(section, 'class_number'),
					getattr(section, 'term_year'), getattr(section, 'open_only'))
			#print('' + available_sections.__str__() + '\n\n')
			if available_sections != None:
				for available_section in available_sections:
					output_file.write('AVAILABLE: ' + available_section.__str__() + '\n')
		webbrowser.open(output_file_name)
		time.sleep(delay)