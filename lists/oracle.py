import ipaddress
import json

# https://docs.cloud.oracle.com/en-us/iaas/tools/public_ip_ranges.json

def check(ips):
	if isinstance(ips, str):
		ips = [ips]

	# Initialize results
	results = []

	# Load json data
	with open("data/oracle.json", "r") as f:
		data = json.loads(f.read())
		f.close()

	# Loop through all regions
	for region_data in data['regions']:
		region = region_data['region']

		# Loop through each CIDR block
		for block in region_data['cidrs']:
			# Loop through each IP
			for ip in ips:
				cidr = block['cidr']
				service = "/".join(block['tags'])

				if ipaddress.ip_address(ip) in ipaddress.ip_network(cidr):
					results.append({
						'ip': ip,
						'provider': 'oracle',
						'service': service,
						'region': region
						})

	return results