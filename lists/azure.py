import ipaddress
import json

# https://download.microsoft.com/download/7/1/D/71D86715-5596-4529-9B13-DA13A5DE5B63/ServiceTags_Public_20200420.json
# https://download.microsoft.com/download/6/4/D/64DB03BF-895B-4173-A8B1-BA4AD5D4DF22/ServiceTags_AzureGovernment_20200420.json

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