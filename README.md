Instructions:
1. Timeular:
	- Go to timeular (app) profile [link: https://profile.timeular.com/#/login]
	- On 'Integrations', download the iCal version of your logged hours
2. Script:
	- Download or copy/paste timeular_ical_parser.py from this repo
	- Open in text editor, and edit fields below "if '__name__' == '__main__':"
		- You'll need to look up the time difference between yourself and UTC. For example, I'm MST, which is (currently) 6 hours behind, hence the "-6"
		- start_date and end_date inputs take time change into account
		- If one time spans two days, the start date (before midnight) will be used for the date filter
	- Run from command line (make sure you're using python 3: 'python tiemular_ical_parser.py'
3. Use in Excel:
	- Open output file location
	- Right click new file -> open with Excel
	- Manipulate as needed