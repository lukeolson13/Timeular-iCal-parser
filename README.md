Instructions:
1. Timeular:
	- Go to [timeular (app) profile](https://profile.timeular.com/#/login)
	- On 'Integrations', download the iCal version of your logged hours (by going to the URL that's generated)
2. Script:
	- Download or copy/paste timeular_ical_parser.py from this repo
	- Open in text editor, and edit time difference field below "if '__name__' == '__main__':"
		- You'll need to look up the time difference between yourself and UTC. For example, I'm MST, which is (currently) 6 hours behind, hence the "-6"
	- Run from command line (make sure you're using python 3): 'python tiemular_ical_parser.py <iCal input file> <csv output file to generate>'
	- Add option start and end dates:
		- Date inputs take time change into account
		- If one time spans two days, the start date (before midnight) will be used for the date filter
3. Use in Excel:
	- Open output file location
	- Right click new file -> open with Excel
	- Manipulate as needed