# thanks Jeff Wintersinger for the inspiration
# see https://github.com/jwintersinger/groceryslots

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
		print('request returned error:')
		print(r.reason)
	return r.json()

def fetch_nearby_locations(lat, lng, date, distance=25, dose=2):
	url = f'https://api.covaxonbooking.ca/public/locations/search'
	json = {
		'clientTimeZone': "America/Toronto",
		'doseNumber': dose,
		'externalAppointments': [
			{
				'doseNumber': 1,
				'start': '2021-09-15',
				'isSingleDose': False,
			}],
		'location': {
			'lat': lat,
			'lng': lng
		},
		'fromDate': date,
		'groupSize': 1,
		'locationQuery': {'includePools': ['default'], 'includeTags': [], 'excludeTags': ["a154t0000004hFFAAY"]},
		'locationType': "CombinedBooking",
		'radiusUnit': "km",
		'radiusValue': distance,
		'timeZone': "America/Toronto",
		'vaccineData': 'WyJhMWQ0dDAwMDAwMDFqZGtBQUEiXQ==',
	}
	return fetch(url, json)

def fetch_available_dates(location, startDate, endDate, dose=2):
	url = f'https://api.covaxonbooking.ca/public/locations/{location}/availability'
	json = {
		'startDate': startDate,
		'endDate': endDate,
		'vaccineData':'WyJhMWQ0dDAwMDAwMDFqZGtBQUEiXQ==',
		'doseNumber':dose,
	}
	return fetch(url, json)

def fetch_available_times(location, date):
	url = f'https://api.covaxonbooking.ca/public/locations/{location}/date/{date}/slots'
	json = {
		'vaccineData':'WyJhMWQ0dDAwMDAwMDFqZGtBQUEiXQ==',
	}
	return fetch(url, json)

def main():
	parser = argparse.ArgumentParser(
		description='Ontario mass vaccination clinics for availability',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter
	)
	parser.add_argument('location',
		help='either location id such as a0h4t0000006cHHAAY, or "lat,long" to search for nearby locations')
	parser.add_argument('--start', default='2022-01-05',
		help='start date in YYYY-MM-DD format')
	parser.add_argument('--end', default='2022-03-06',
		help='end date in YYYY-MM-DD format')
	parser.add_argument('--distance', type=int, default=25,
		help='Maximum distance to search for available clinics')

	args = parser.parse_args()

	location = args.location
	if not location.isalnum() and location.count(',') != 1:
		print(f'invalid location: {location}')
		return
	if not location.isalnum() and location.count(',') == 1:
		locations_response = fetch_nearby_locations(*[float(S) for S in location.split(',')], date=args.start, distance=args.distance)
		onl_booking_locations = [S for S in locations_response['locations'] if S['type'] == 'OnlineBooking']
		
		print(f'{len(locations_response["locations"])} clinics found within {args.distance}km')
		print(f'{len(onl_booking_locations)} available clinics with online booking through portal')
		for idx, loc in enumerate(onl_booking_locations[:10]):
			print(f'[{idx}]: {loc["distanceInMeters"]/1000:.2f}km,\t{loc["name"]}')
		print('')

		if not onl_booking_locations:
			print('Locations with third party booking:')
			for loc in (S for S in locations_response['locations'] if S['type'] == 'ThirdPartyBooking'):
				print(f'  {loc["distanceInMeters"]/1000:.2f}km\t{loc["name"]} :\t{loc["externalURL"]}')
			return

		idx = int(input('Please pick a location: '))
		location = onl_booking_locations[idx]['extId']
		print(f'location id: {location}\n')

	dates_response = fetch_available_dates(location, args.start, args.end)

	avail_dates = [S['date'] for S in dates_response['availability'] if S['available']]
	print(f'available dates: {avail_dates}')

	for date in avail_dates[:3]:
		times_response = fetch_available_times(location, date)
		avail_times = [S['localStartTime'][:5] for S in times_response['slotsWithAvailability']]
		print(f'available times for {date}: {avail_times}')

	#TODO: Announce via Chromecast when a new spot opens using saytext.py

if __name__ == '__main__':
  main()
