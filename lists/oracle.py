import ipaddress
import json
import requests

# https://docs.cloud.oracle.com/en-us/iaas/tools/public_ip_ranges.json

def update():
	results = []

	response = requests.get('https://docs.cloud.oracle.com/en-us/iaas/tools/public_ip_ranges.json')

	if response.status_code != 200:
		return False

	data = json.loads(response.text)

	for region_info in data['regions']:
		region = region_info['region']

		for cidr_info in region_info['cidrs']:
			cidr = cidr_info['cidr']
			service = "/".join(cidr_info['tags'])

			results.append("%s %s %s %s" % (cidr, 'oracle', service, region))


	# Write results to file
	with open('data/oracle.txt', 'w') as f:
		f.write("\n".join(results))
		f.close()

	return len(results)