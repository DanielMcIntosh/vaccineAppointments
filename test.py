import requests
import sys
import argparse

def make_header():
	headers = {
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0',
		'Accept': 'application/json, text/plain, */*',
		'Accept-Language': 'en-CA,en-US;q=0.9,en-GB;q=0.8,en;q=0.7' ,
		'Content-Type': 'application/json;charset=utf-8',
	}
	return headers

def fetch(url, json):
	r = requests.post(url, json=json, headers=make_header())
	if r.status_code != 200:
		print("request returned error:")
		print(r.reason)
	return r.json()

def fetch_available_dates(location, startDate, endDate, dose=1):
	json = {
		'startDate': startDate,
		'endDate': endDate,
		'vaccineData':'WyJhMWQ0dDAwMDAwMDFqZGtBQUEiXQ==',
		'doseNumber':dose,
	}
	url = 'https://api.covaxonbooking.ca/public/locations/%s/availability' % location
	return fetch(url, json)

#location query:
#https://api.covaxonbooking.ca/public/locations/search
#{"location":{"lat":43.7744758,"lng":-79.2551582},"fromDate":"2021-05-04","vaccineData":"WyJhMWQ0dDAwMDAwMDFqY0lBQVEiLCJhMWQ0dDAwMDAwMDFqaUxBQVEiLCJhMWQ0dDAwMDAwMDFrOVpBQVEiLCJhMWQ0dDAwMDAwMDFrTVNBQVkiLCJhMWQ0dDAwMDAwMDFrWGtBQUkiLCJhMWQ0dDAwMDAwMDFrWHBBQUkiLCJhMWQ0dDAwMDAwMDFrZzhBQUEiLCJhMWQ0dDAwMDAwMDFrdTdBQUEiLCJhMWQ0dDAwMDAwMDFaSGxBQU0iLCJhMWQ0dDAwMDAwMDFaSG1BQU0iLCJhMWQ0dDAwMDAwMDFnbzdBQUEiLCJhMWQ0dDAwMDAwMDFoMkVBQVEiLCJhMWQ0dDAwMDAwMDFpbnhBQUEiLCJhMWQ0dDAwMDAwMDFqZGtBQUEiXQ==","locationQuery":{"includePools":["default"]},"doseNumber":1}

#slots query:
#https://api.covaxonbooking.ca/public/locations/a0h4t0000006Oo9AAE/date/2021-05-04/slots
#{"vaccineData":"WyJhMWQ0dDAwMDAwMDFqZGtBQUEiXQ=="}

def main():
	parser = argparse.ArgumentParser(
		description='Ontario mass vaccination clinics for availability',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter
	)
	parser.add_argument('--location', default='a0h4t0000006OqyAAE',
		help='Location (e.g. a0h4t0000006OqyAAE, or a0h4t0000006Oo9AAE)')
	parser.add_argument('--start', default='2021-05-04',
		help='start date in YYYY-MM-DD format')
	parser.add_argument('--end', default='2021-05-31',
		help='end date in YYYY-MM-DD format')
	args = parser.parse_args()

	response = fetch_available_dates(args.location, args.start, args.end)

	avail = [S['date'] for S in response['availability'] if S['available']]
	print(avail)

	print("\n\n\n")

	print(response)

if __name__ == '__main__':
  main()
