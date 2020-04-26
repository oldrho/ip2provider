import ipaddress
import json


def check(ips):
	if isinstance(ips, str):
		ips = [ips]

	files = ['data/azure.json','data/azure-gov.json']

	# Initialize results
	results = []


	# Load json data
	for file in files:
		with open(file, "r") as f:
			data = json.loads(f.read())
			f.close()

		# Loop through service groups
		for group in data['values']:
			try:
				service = group['properties']['systemService']
				region = group['properties']['region']

				# Loop through CIDR addresses
				for cidr in group['properties']['addressPrefixes']:

					# Loop through target IPs
					for ip in ips:
						if ipaddress.ip_address(ip) in ipaddress.ip_network(cidr):
							results.append({
								"ip": ip,
								"provider":"azure",
								"service":service,
								"region":region
								})
			except:
				True # NOOP

	return results