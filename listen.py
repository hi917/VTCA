from pyvt import Timetable
import datetime
import os
import sys
import time
import webbrowser
import winsound

# Alerter settings/IO
delay = 10
input_file_name = 'listening_list.txt'
output_file_name = 'available_sections.txt'

# Duration and frequency of beep
duration = 1000
frequency = 1500

# Program flags
VERBOSE = False
MORE_VERBOSE = False

# Print to stdout and flush stdout
def printf(string):
	print(str(string))
	sys.stdout.flush()

# Process arguments for delay, input, and output
# param_offset == 1 if no flags, == 2 if there are flags
def processDelayAndIO(param_offset):
	if len(sys.argv) >= param_offset + 1:
		global delay
		delay = int(sys.argv[param_offset])
	# File containing sections to listen to
	if len(sys.argv) >= param_offset + 2:
		global input_file_name
		input_file_name = sys.argv[param_offset + 1]
	# File containing available sections
	if len(sys.argv) >= param_offset + 3:
		global output_file_name
		output_file_name = sys.argv[param_offset + 2]

# Usage information
if  len(sys.argv) >= 2:
	if (sys.argv[1] == '-help' or sys.argv[1] == '-h' or sys.argv[1] == '--help' or sys.argv[1] == '--h'):
		print('Usage: listen.py [-dDvV] [delay] [infile] [outfile]\n\t'
			+ '-d: Set beep duration to 5s (default 1s)\n\t'
			+ '-D: Set beep duration to 10s (default 1s)\n\t'
			+ '-v: Run program in verbose mode\n\t'
			+ '-V: Run program in more verbose mode\n\t'
			+ 'delay: Specify delay for checking course availabilities (in seconds)\n\t'
			+ 'infile: The directory of the .txt file with courses to check availabilities\n\t'
			+ 'outfile: The directory of the .txt file with availability information')
		sys.exit()

# Process flags, delay, and IO
if sys.argv[1][0] == '-':
	flags = list(sys.argv[1][1:])
	for flag in flags:
		if flag == 'd': # Make beep duration long
			duration = 5000
		if flag == 'D': # Make beep duration even longer
			duration = 10000
		if flag == 'v': # Print details about alerter
			VERBOSE = True
		if flag == 'V': # Print even more details about alerter
			MORE_VERBOSE = True
	processDelayAndIO(2)
else:
	processDelayAndIO(1)

# Signal user process settings
if MORE_VERBOSE:
	printf('Running program in (more) verbose mode')
elif VERBOSE:
	printf('Running program in verbose mode')
printf('Beep alert duration ' + str(duration/1000)+ 's')

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
		if len(parts) != 6 or len(parts[0]) != 5:
			continue
		parts[5] = parts[5].strip('\n')
		section = Section(parts[0], parts[1], parts[2], parts[3], parts[4], parts[5]);
		if len(getattr(section, 'crn_code')) < 5:
			setattr(section, 'crn_code', '')
		sections.append(section)
		if VERBOSE or MORE_VERBOSE:
			printf('[' + str(datetime.datetime.now()) + '] Listening for ' + str(section))

timetable = Timetable()
# Allow loop if listening to classes
if (len(sections) > 0):
	printf('[' + str(datetime.datetime.now()) + '] Initiated alerter')

	while (True):
		open_section = False
		output_file = open(output_file_name, 'w')

		for section in sections:
			available_sections = []

			# Lookup section by crn if available
			if getattr(section, 'crn_code'):
				if MORE_VERBOSE:
					printf('[' + str(datetime.datetime.now()) + '] Timetable lookup via CRN (' + getattr(section, 'crn_code') + ')')
				available_sections = timetable.refined_lookup(getattr(section, 'crn_code'), getattr(section, 'term_year'), getattr(section, 'open_only'))
			# Lookup section by subject code and clas number
			elif getattr(section, 'subject_code') and getattr(section, 'class_number'):
				if MORE_VERBOSE:
					printf('[' + str(datetime.datetime.now()) + '] Timetable lookup via subject and class number (' + getattr(section, 'subject_code') 
						+ '-' + getattr(section, 'class_number') + ')')
				available_sections = timetable.class_lookup(getattr(section, 'subject_code'), getattr(section, 'class_number'),
					getattr(section, 'term_year'), getattr(section, 'open_only'))

			if available_sections != None:
				if VERBOSE or MORE_VERBOSE:
					printf('[' + str(datetime.datetime.now()) + '] Available section(s) found')
				open_section = True
				# Write all available sections to output file
				for available_section in available_sections:
					output_file.write('AVAILABLE: ' + available_section.__str__() + '\n')
					if VERBOSE or MORE_VERBOSE:
						printf('[' + str(datetime.datetime.now()) + '] Found section (' + str(available_section) + ')')

		# Notify user of available section via beep, console, and output file opening
		if open_section:
			webbrowser.open(output_file_name)
			winsound.Beep(frequency, duration)
			if VERBOSE or MORE_VERBOSE:
				printf('[' + str(datetime.datetime.now()) + '] Opened available sections file...')

		time.sleep(delay)
		if VERBOSE or MORE_VERBOSE:
			printf('[' + str(datetime.datetime.now()) + '] Sleeping for ' + str(delay) +'s')