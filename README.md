Instructions:
1. Timeular:
	- Go to [timeular (app) profile](https://profile.timeular.com/#/login)
	- On 'Integrations', click the iCal version of your logged hours and copy the URL
2. Script:
	- Download or copy/paste timeular_ical_parser.py from this repo
	- Open in text editor, and edit the input_url, output_folder, and time difference field below "if '__name__' == '__main__':"
		- Paste the ical URL in the "input_url" field
		- Add a folder location where you want your generated file to end up, or leave blank to have it generate wherever you run the script from
	- Run from command line (make sure you're using python 3): 'python tiemular_ical_parser.py'
	- Add optional start and end dates:
		- Date inputs take time change into account
		- If one time spans two days, the start date (before midnight) will be used for the date filter
3. Use in Excel:
	- Open output file location
	- Right click new file -> open with Excel
	- Manipulate as needed