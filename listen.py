from pyvt import Timetable
from Section import Section
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
DEBUG = False
SINGLE = False
MULTIPLE = False

# Get current date and time
def currTime():
	return '[' + str(datetime.datetime.now()) + ']'

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

# Display usage when -h and --help flagged
if len(sys.argv) >= 2 and (sys.argv[1] == '-h' or sys.argv[1] == '--help'):
	print('usage: listen.py [-bBdmsvV] [delay] [infile] [outfile]\n\t'
		+ '-b: Set beep duration to 5s (default 1s)\n\t'
		+ '-B: Set beep duration to 10s (default 1s)\n\t'
		+ '-d: Run program in debug mode\n\t'
		+ '-m: Print to stdout available course found multiple times (x5). Must be in verbose or more verbose mode to see.\n\t'
		+ '-s: Run program once\n\t'
		+ '-v: Run program in verbose mode\n\t'
		+ '-V: Run program in more verbose mode\n\t'
		+ 'delay: Specify delay for checking course availabilities (in seconds)\n\t'
		+ 'infile: The directory of the .txt file with courses to check availabilities\n\t'
		+ 'outfile: The directory of the .txt file with availability information\n\n\t'

		+ 'Program Mode Information Table:\n\t'
		+ '                 | N | V | MV | D |\n\t'
		+ 'Globals          |   |   |    | X |\n\t'
		+ 'Parts Information|   |   |    | X |\n\t'
		+ 'Parts Continued  |   |   |    | X |\n\t'
		+ 'Course Detection |   |   |    | X |\n\t'
		+ 'New Course Listen|   | X | X  | X |\n\t'
		+ 'All Course Listen|   |   |    | X |\n\t'
		+ 'CRN Srch Msg     |   |   | X  | X |\n\t'
		+ 'CRN Rslt Msg     |   |   |    | X |\n\t'
		+ 'Course Srch Msg  |   |   | X  | X |\n\t'
		+ 'Course Srch Rslt |   |   |    | X |\n\t'
		+ 'Open Course Found|   | X | X  | X |\n\t'
		+ 'Open Outfile     |   | X | X  | X |\n\t'
		+ 'Sleep Msg        |   | X | X  | X |\n\t'
	)
	sys.exit()

# Process flags, delay, and IO
if len(sys.argv) >= 2 and sys.argv[1][0] == '-':
	flags = list(sys.argv[1][1:])
	for flag in flags:
		if flag == 'b': # Make beep duration long (5s)
			duration = 5000
		if flag == 'B': # Make beep duration even longer (10s)
			duration = 10000
		if flag == 'v': # Print details about alerter
			VERBOSE = True
		if flag == 'V': # Print even more details about alerter
			MORE_VERBOSE = True
		if flag == 'd' or flag == 'D': # Debug mode, intended for developer use
			VERBOSE = True
			MORE_VERBOSE = True
			DEBUG = True
		if flag == 's': # Run program for only a single course check
			SINGLE = True
		if flag == 'm': # Print to stdout available course found multiple times (x5). Must be in verbose or more verbose mode to see.
			MULTIPLE = True
	processDelayAndIO(2)
else:
	processDelayAndIO(1)

# Signal user process settings
if DEBUG:
	printf('==================================================')
	printf('Program Variables:')
	printf('\tdelay: ' + str(delay))
	printf('\tinput_file_name: ' + str(input_file_name))
	printf('\toutput_file_name: ' + str(output_file_name))
	printf('\tduration: ' + str(duration))
	printf('\tfrequency: ' + str(frequency))
	printf('==================================================')
elif MORE_VERBOSE:
	printf('Running program in (more) verbose mode')
elif VERBOSE:
	printf('Running program in verbose mode')
if not DEBUG:
	printf('Beep alert duration ' + str(duration/1000)+ 's')

#List of actively listening courses
sections = []

#Read section list via input file
with open(input_file_name) as inputFile:
	for line in inputFile:
		parts = line.split('|')
		if DEBUG:
			printf('Found parts: [' + line[0:len(line)-1] + '] which has length ' + str(len(parts)))
		bad_term = False
		curr_year = datetime.datetime.now().year
		# Determine if valid term year and term months
		if len(parts) > 3 and (len(parts[4]) != 6 or (parts[4][4:] != '01' and parts[4][4:] != '06' and parts[4][4:] != '07' and parts[4][4:] != '09') or int(curr_year) > int(parts[4][:4])):
			bad_term = True
		# Ignore line if not enough parts, line starts with #, CRN has 1-4 digits (inclusive), CRN has more than 5 digits, or open_only != true and != false
		if len(parts) != 6 or (len(parts[0]) > 0 and parts[0][0] == '#') or (len(parts[0]) < 5 and len(parts[0]) > 0) or len(parts[0]) > 5 or (parts[5].strip('\n') != 'true' and parts[5].strip('\n') != 'false') or bad_term:
			if DEBUG and len(parts) == 6:
				printf('\nParts length: ' + str(len(parts)))
				printf('CRN has more than zero digits and starts with #: ' + str((len(parts[0]) > 0 and parts[0][0] == '#')))
				printf('CRN has 1-4 digits (incl): ' + str((len(parts[0]) < 5 and len(parts[0]) > 0)))
				printf('CRN has more than 5 digits: ' + str(len(parts[0]) > 5))
				printf('open_only is not \'true\' or \'false\': ' + str(parts[5].strip('\n') != 'true' and parts[5].strip('\n') != 'false'))
				printf('bad_term: ' + str(bad_term))
				printf('Continuing course parsing when parts: [' + line[0:len(line)-1] + ']\n')
			continue
		parts[5] = parts[5].strip('\n')
		if DEBUG:
			printf('Course detected: ' + parts[0] + ' ' + parts[1] + ' ' + parts[2] + ' ' + parts[3] + ' ' + parts[4] + ' ' + parts[5].title())
		section = Section(str(parts[0]), parts[1], parts[2], parts[3], parts[4], parts[5]);
		sections.append(section)
		if VERBOSE or MORE_VERBOSE:
			printf(currTime() + ' Listening for ' + str(section))

if DEBUG:
	printf('\nSections Listening To:')
	for section in sections:
		printf(section)
	printf('')

timetable = Timetable()
# Allow loop if listening to classes
if (len(sections) > 0):
	printf(currTime() + ' Initiated alerter')

	while (True):
		open_section = False
		output_file = open(output_file_name, 'w')

		for section in sections:
			available_sections = []

			# Lookup section by crn if available and valid
			if len(getattr(section, 'crn_code')) == 5:
				try:
					available_sections = timetable.crn_lookup(getattr(section, 'crn_code'), getattr(section, 'term_year'), getattr(section, 'open_only'));
				except Exception as e:
					printf(gettime() + ' An exception has occured: ' + str(e));

				if DEBUG:
					printf(currTime() + ' Timetable lookup via CRN (' + getattr(section, 'crn_code') + ') produced ' + str(available_sections))
				elif MORE_VERBOSE:
					if VERBOSE or MORE_VERBOSE:
						printf(currTime() + ' Timetable lookup via CRN (' + getattr(section, 'crn_code') + ')')
					else:
						pass
			# Lookup section by subject code
			elif getattr(section, 'subject_code') and getattr(section, 'class_number'):
				try:
					available_sections = timetable.class_lookup(getattr(section, 'subject_code'), getattr(section, 'class_number'),
						getattr(section, 'term_year'), getattr(section, 'open_only'))
				except Exception as e:
					if VERBOSE or MORE_VERBOSE:
						printf(gettime() + ' An exception has occured: ' + str(e));
					else:
						pass

				if DEBUG:
					printf(currTime() + ' Timetable lookup via subject and class number (' + getattr(section, 'subject_code') 
						+ '-' + getattr(section, 'class_number') + ') produced ' + str(available_sections))
				elif MORE_VERBOSE:
					printf(currTime() + ' Timetable lookup via subject and class number (' + getattr(section, 'subject_code') 
						+ '-' + getattr(section, 'class_number') + ')')

			# Section(s) found from lookup
			if available_sections != None:
				if VERBOSE or MORE_VERBOSE:
					printf(currTime() + ' Available section(s) found')
				open_section = True
				# Write all available sections to output file
				if isinstance(available_sections, list):
					for available_section in available_sections:
						output_file.write('AVAILABLE: ' + available_section.__str__() + '\n')
						output_file.flush()

						if VERBOSE or MORE_VERBOSE:
							printf(currTime() + ' Found section (' + str(available_section) + ')')
							if MULTIPLE:
								printf(currTime() + ' Found section (' + str(available_section) + ')')
								printf(currTime() + ' Found section (' + str(available_section) + ')')
								printf(currTime() + ' Found section (' + str(available_section) + ')')
								printf(currTime() + ' Found section (' + str(available_section) + ')')

				else:
					output_file.write('AVAILABLE: ' + available_sections.__str__() + '\n')
					output_file.flush()

					if VERBOSE or MORE_VERBOSE:
						printf(currTime() + ' Found section (' + str(available_sections) + ')')
						if MULTIPLE:
							printf(currTime() + ' Found section (' + str(available_sections) + ')')
							printf(currTime() + ' Found section (' + str(available_sections) + ')')
							printf(currTime() + ' Found section (' + str(available_sections) + ')')
							printf(currTime() + ' Found section (' + str(available_sections) + ')')

		# Notify user of available section via beep, console, and output file opening
		if open_section:
			webbrowser.open(output_file_name)
			winsound.Beep(frequency, duration)

			if VERBOSE or MORE_VERBOSE:
				printf(currTime() + ' Opened available sections file...')

		if SINGLE:
			printf(currTime() + ' Single coruse check complete, exiting.')
			sys.exit()

		if VERBOSE or MORE_VERBOSE:
			printf(currTime() + ' Sleeping for ' + str(delay) +'s')
		time.sleep(delay)