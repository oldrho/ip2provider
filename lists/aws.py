import ipaddress
import json
import requests

# https://ip-ranges.amazonaws.com/ip-ranges.json

def update():
	results = []

	response = requests.get('https://ip-ranges.amazonaws.com/ip-ranges.json')

	if response.status_code != 200:
		return False

	data = json.loads(response.text)

	def process_json(section):
		nonlocal results,data

		for group in data[section]:
			cidr = group['ip_prefix'] if 'ip_prefix' in group.keys() else group['ipv6_prefix']

			results.append("%s %s %s %s" % (cidr, 'aws', group['service'], group['region']))

	process_json('prefixes')
	process_json('ipv6_prefixes')


	# Write to file
	with open('data/aws.txt', 'w') as f:
		f.write("\n".join(results))
		f.close()

	return len(results)