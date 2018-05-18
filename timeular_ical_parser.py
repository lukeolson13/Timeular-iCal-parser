#!/usr/bin/env python
'''
Parse Timeular ical export and create csv
'''

__author__ = 'Luke Olson'

from datetime import datetime, timedelta
import pandas as pd
import requests
from sys import argv

def get_string_dates():
	'''
	Ask for user input on range of dates to get
	Returns:
		String dates for start and end, or None if not specified
	'''
	start = input('Enter a start date, or skip for all (MM-DD-YYYY): ')
	end = input('Enter an end date, or skip for all (MM-DD-YYYY): ')
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
	date = date_time.strftime('%m-%d-%Y')
	time = date_time.strftime('%H:%M:%S')
	return date_time, date, time

def get_date(str_date):
	'''
	Get datetime date from string date
	Inputs:
		str_date - string date in format 'MM-DD-YYYY'
	Returns:
		Datetime date
	'''
	return datetime.strptime(str_date, '%m-%d-%Y')

def get_dt_dates(start_in, end_in):
	'''
	Get datetime version of dates
	Inputs:
		start_in - string version of start date
		end_in - string version of end date
	Returns:
		start_out - datetime version of start date
		end_out - datetime version of end date
	'''
	if start_in:
		start_out = get_date(start_in)
	else:
		start_out = None

	if end_in:
		end_out = get_date(end_in)
	else:
		end_out = None

	return start_out, end_out

def get_entries(ical_url):
	'''
	Get iCal data from URL
	Inputs:
		ical_url - iCal URL found in Timeular profile
	Returns:
		Data from iCal
	'''
	data = requests.get(ical_url)
	decoded = data.content.decode('utf-8')
	return decoded.split('\r\n')

def get_time_diff():
	'''
	Determine difference in time between local timezone (of system running
		script) and UTC (timezone of iCal)
	Returns:
		Difference (in hours) between local time and UTC
	'''
	local = datetime.now()
	utc = datetime.utcnow()
	diff = (local - utc).days * 24 + round((local - utc).seconds, -1) / 3600
	return int(diff)

def parse_ical(ical_url, start, end):
	'''
	Create pandas dataframe from parsed ical Timeular entries
	Inputs:
		ical_url - URL of ical file containing Timeular entries
		start - first day to include in output
		end - last day to include in output
	Returns:
		Pandas dataframe sorted by date and time
	'''
	df = pd.DataFrame(columns=['start day', 'start time', 'end time', 'hours', 'summary', 'description'])

	entry_list = get_entries(ical_url)

	time_diff = get_time_diff()

	skip = False
	for line in entry_list:
		if (':' not in line):
			# Protect against new line oddities, among others
			continue

		split = line.split(':')
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

def get_output_file(output_folder, start_date, end_date):
	'''
	Create full file path, including file name. Output depends on date inputs
	Inputs:
		output_folder - folder to create file in (relative to current
			directory where script is being run)
		start_date - user input on date to begin with
		end_date - user input on date to end with
	Returns:
		Full file path
	'''
	if output_folder[-1] != '/':
		output_folder += '/'

	if start_date:
		start_out = start_date
	else:
		start_out = 'Everything'

	if end_date:
		end_out = end_date
	else:
		end_out = datetime.now().strftime("%m-%d-%Y_%H%M")

	return '{}{}_to_{}.csv'.format(output_folder, start_out, end_out)

def export_to_csv(df, output_file):
	'''
	Export pandas dataframe to CSV
	Inputs:
		df - pandas dataframe
		output-file - location and name of output file
	'''
	df.to_csv(output_file, index=False)
	print('Success! Check the file location: {}'.format(output_file))

def main(ical_url, output_folder):
	'''
	Execute above functions
	Inputs:
		ical_url - URL of ical file containing Timeular entries
		output_folder - folder location to output CSV to
	'''
	start, end = get_string_dates()
	start_date, end_date = get_dt_dates(start, end)

	df = parse_ical(ical_url, start_date, end_date)
	tot_hours = sum(df['hours'].values)
	print('Total hours during this period: {}'.format(round(tot_hours, 3)))
	# can manipulate pandas dataframe here if needed

	if output_folder:
		output_file = get_output_file(output_folder, start, end)
		export_to_csv(df, output_file)

if __name__ == '__main__':
	# Required input:
	ical_url = 'https://thirdparty.timeular.com/api/ical/480c0f598f55defd6a8b8e0702c8ddbcd1b1757549840297d7a2fc75880d35fe/calendar.ics'

	# Optional inputs:
	output_folder = '../../hours/excel'

	# Run functions (don't edit)
	main(ical_url, output_folder)