This script is meant to create a CSV output of time logged within the Timeular app. Currently, there is no way to do this without downloading the desktop app, which is only available for Windows and Mac. This allows anyone with Python and an internet connection to easily genenerate an output file (meant to be opened in Excel or similar) with their tracked hours over a set interval of time.

Instructions:
1. Timeular:
	- Go to [timeular (app) profile](https://profile.timeular.com/#/login)
	- On 'Integrations', click the iCal version of your logged hours and copy the URL
2. Script:
	- Download or copy/paste timeular_ical_parser.py from this repo
	- Open in text editor, and edit the input_url and output_folder (optional) below "if '__name__' == '__main__':"
		- Paste the ical URL in the "input_url" field
		- output_folder options:
			- Add a folder location where you want your generated file to end up
			- Set to null ('') or none (None) to not generate file and only get a print out of total hours over that period (for quick reference)
	- Run from command line (make sure you're using python 3): 'python tiemular_ical_parser.py'
	- Add optional start and end dates:
		- Date inputs take time change into account
		- If one time spans two days, the start date (before midnight) will be used for the date filter
3. Use in Excel (if output_folder was given and file was generated):
	- Open output file location
	- Right click new file -> open with Excel
	- Manipulate as needed