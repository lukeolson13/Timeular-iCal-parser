#!/usr/bin/env python
'''
Parse Timeular ical export and create csv
'''

__author__ = 'Luke Olson'

from datetime import datetime, timedelta
import pandas as pd
from sys import argv

def get_dates():
	start = input('Enter a start date, or skip for all (MM/DD/YYYY): ')
	end = input('Enter an end date, or skip for all (MM/DD/YYYY): ')
	return start, end

def ical_date_parse(ical_date_time, time_diff):
	'''
	Convert ical datetime to python datetime
	Inputs:
		ical_date_time - ical formatted datetime as string
		time_diff - difference in time between your time zone and UTC
	Returns:
		date_time - python datetime (as datetime object)
		date -  date (as string)
		time - time (using 24 hour format - as string)
	'''
	date_time = datetime.strptime(ical_date_time, '%Y%m%dT%H%M%SZ')
	date_time += timedelta(hours=time_diff)
	date = date_time.strftime('%m/%d/%Y')
	time = date_time.strftime('%H:%M:%S')
	return date_time, date, time

def get_date(str_date):
	'''
	Get datetime date from string date
	Inputs:
		str_date - string date in format 'MM/DD/YYYY'
	Returns:
		Datetime date
	'''
	return datetime.strptime(str_date, '%m/%d/%Y')

def parse_ical(ical_file, time_diff, start, end):
	'''
	Create pandas dataframe from parsed ical Timeular entries
	Inputs:
		ical_file - location and name of ical file
		time_diff - difference in time between your time zone and UTC
		start - first day to include in output
		end - last day to include in output
	Returns:
		Pandas dataframe sorted by date and time
	'''
	df = pd.DataFrame(columns=['start day', 'start time', 'end time', 'hours', 'summary', 'description'])
	with open(ical_file, 'r+') as f:
		skip = False
		for line in f:
			if (':' not in line):
				# Protect against new line oddities, among others
				continue

			split = line[:-1].split(':')
			if (split[0] == 'BEGIN') and (split[1] == 'VEVENT'):
			    dic = {}
			    skip = False

			if skip:
				continue

			elif split[0] == 'DTSTART':
			    begin_date_time, begin_date, begin_time = ical_date_parse(split[1], time_diff)
			    if start:
				    if get_date(begin_date) < start:
				    	skip = True
				    	continue
			    dic['start day'] = begin_date
			    dic['start time'] = begin_time

			elif split[0] == 'SUMMARY':
			    dic['summary'] = split[1]

			elif split[0] == 'DESCRIPTION':
			    dic['description'] = split[1]

			elif split[0] == 'DTEND':
			    end_date_time, end_date, end_time = ical_date_parse(split[1], time_diff)
			    if end:
			    	if get_date(end_date) > end:
				    	skip = True
				    	continue
			    diff = (end_date_time - begin_date_time).seconds / 60 / 60
			    dic['end time'] = end_time
			    dic['hours'] = round(diff, 3)

			elif (split[0] == 'END') and (split[1] == 'VEVENT'):
				df = df.append(dic, ignore_index=True)

	return df.sort_values(['start day', 'start time'])

def export_to_csv(df, output_file):
	'''
	Export pandas dataframe to CSV
	Inputs:
		df - pandas dataframe
		output-file - location and name of output file
	'''
	df.to_csv(output_file, index=False)
	print('Success! Check the file location: {}'.format(output_file))

def main(time_diff=0):
	'''
	Execute above functions
	Inputs:
		time_diff - difference in time between your time zone and UTC
	'''
	ical_file = argv[1]
	output_file = argv[2]

	start_date, end_date = get_dates()
	if start_date:
		start_date = get_date(start_date)
	if end_date:
		end_date = get_date(end_date)

	df = parse_ical(ical_file, time_diff, start_date, end_date)
	# can manipulate pandas dataframe here if needed
	export_to_csv(df, output_file)

if __name__ == '__main__':
	# Optional input:
	time_diff = -6

	# Run functions (don't edit)
	main(time_diff)