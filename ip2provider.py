#!/usr/bin/env python3

import argparse
import logging
import sys

import json

import lists.azure as azure
import lists.aws as aws
import lists.gcp as gcp
import lists.oracle as oracle




def main():
	log = logging.getLogger()
	log.setLevel(logging.INFO)
	stream = logging.StreamHandler(sys.stderr)
	stream.setLevel(logging.DEBUG)


	# Arguments
	parser = argparse.ArgumentParser(add_help=True, description='Resolves IPs to their provider details')

	parser.add_argument(
		'ip',
		action='store',
		help='IP(s) to look up (comma separated)'
		)
	parser.add_argument(
		'-o',
		'--output',
		action='store',
		help='Output format',
		default='text'
		)

	args = parser.parse_args()
	output_type = None

	# Addresses
	if not args.ip:
		log.error('Must specify at least one IP address')
		sys.exit(1)

	# Output format
	output_formats = ['text','json','raw']
	if args.output not in output_formats:
		log.error("Must choose a valid output format: " + ", ".join(output_formats))
		sys.exit(1)



	# Results
	results = check(args.ip.split(','))
	if args.output != 'raw':
		results = results_clean(results)
	output(results, args.output)
# End of main





def check(ips):
	if isinstance(ips, str):
		ips = [ips]


	# Check each provider
	checks = []
	checks += azure.check(ips)
	checks += aws.check(ips)
	checks += gcp.check(ips)
	checks += oracle.check(ips)

	return checks

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

	if current['provider'] is not new['provider']:
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





if __name__ == '__main__':
	main()