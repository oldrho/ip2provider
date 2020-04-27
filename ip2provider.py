#!/usr/bin/env python3

import argparse
import logging
import sys
import select
import json
import glob
import ipaddress

import lists.asns as asns
import lists.aws as aws
import lists.azure as azure
import lists.gcp as gcp
import lists.oracle as oracle




def main():
	log = logging.getLogger()
	log.setLevel(logging.INFO)
	stream = logging.StreamHandler(sys.stderr)
	stream.setLevel(logging.DEBUG)

	ips = []


	# Arguments
	parser = argparse.ArgumentParser(add_help=True, description='Resolves IPs to their provider details')

	parser.add_argument(
		'ip',
		action='store',
		help='IP(s) to look up (comma separated)',
		nargs='?'
		)
	parser.add_argument(
		'-o',
		'--output',
		action='store',
		help='Output format',
		default='text'
		)
	parser.add_argument(
		'--update-lists',
		action='store_true',
		help='Update route lists'
		)

	args = parser.parse_args()
	output_type = None


	# Updates
	if args.update_lists:
		update()
		return

	# Addresses
	if not args.ip:
		# Check if we're using stdin
		if select.select([sys.stdin,],[],[],0.0)[0]:
			for ip in sys.stdin:
				ips.append(ip.rstrip())

		# No IPs specified
		else:
			log.error('Must specify at least one IP address')
			sys.exit(1)
	else:
		ips = args.ip.split(',')

	# Output format
	output_formats = ['text','json','raw']
	if args.output not in output_formats:
		log.error("Must choose a valid output format: " + ", ".join(output_formats))
		sys.exit(1)


	# Results
	results = check(ips)
	if args.output != 'raw':
		results = results_clean(results)
	output(results, args.output)
# End of main





def check(ips):
	if isinstance(ips, str):
		ips = [ips]

	# Initialize results
	results = []

	# Files
	files = glob.glob('data/*')

	def check_file(file):
		nonlocal results
		
		# Load json data
		with open(file, "r") as f:
			data = f.read().splitlines()
			f.close()

		# Loop each route
		for route in data:
			(cidr,provider,service,region) = route.split()

			# Loop each IP
			for ip in ips:
				if ipaddress.ip_address(ip) in ipaddress.ip_network(cidr):
					results.append({
						'ip': ip,
						'provider': provider,
						'service': service,
						'region': region
						})

	for file in files:
		check_file(file)

	return results

def results_clean(results):

	cleaned = {}

	# Filter duplicates
	for result in results:
		ip = result['ip']

		# Never seen before
		if ip not in cleaned.keys():
			cleaned[ip] = result.copy()
			continue

		# Merge into existing result
		result_merge(cleaned[ip], result)


	# Find any unset fields
	for result in cleaned.values():
		result['service'] = 'unknown' if not result['service'] else result['service']
		result['region'] = 'unknown' if not result['region'] else result['region']

	return cleaned

def result_merge(current, new):
	current['service'] = new['service'] if not current['service'] and new['service'] else current['service']
	current['region'] = new['region'] if (not current['region'] and new['region']) else current['region']

	if current['provider'] != new['provider']:
		current['provider'] = 'conflict'





def output(data, type, fields=None):
	if type == 'text':
		return output_text(data)
	if type == 'json':
		return output_json(data)
	if type == 'raw':
		return output_raw(data)

def output_text(data):
	for entry in data.values():
		print(" ".join(entry.values()))

def output_json(data):
	print(json.dumps(list(data.values())))

def output_raw(data):
	print(data)





def update():
	total = 0

	total += asns.update()
	total += aws.update()
	total += azure.update()
	total += gcp.update()
	total += oracle.update()

	print("Updated %d entries" % (total))


if __name__ == '__main__':
	main()