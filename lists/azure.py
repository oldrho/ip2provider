import ipaddress
import json
import requests

# https://download.microsoft.com/download/7/1/D/71D86715-5596-4529-9B13-DA13A5DE5B63/ServiceTags_Public_20200420.json
# https://download.microsoft.com/download/6/4/D/64DB03BF-895B-4173-A8B1-BA4AD5D4DF22/ServiceTags_AzureGovernment_20200420.json

def update():
	results = []

	def update_azure(provider, url, file):
		nonlocal results


		# Get JSON data from Azure
		response = requests.get(url)
		if response.status_code != 200:
			return False
		data = json.loads(response.text)


		# Process service groups
		for group in data['values']:
			service = group['properties']['systemService']
			region = group['properties']['region']

			if not service or not region:
				continue

			for cidr in group['properties']['addressPrefixes']:
				results.append("%s %s %s %s" % (cidr, provider, service, region))


		# Write to file
		with open(file, 'w') as f:
			f.write("\n".join(results))
			f.close()

		return len(results)



	count = 0
	clouds = [
		['azure', 'https://download.microsoft.com/download/7/1/D/71D86715-5596-4529-9B13-DA13A5DE5B63/ServiceTags_Public_20200420.json', 'data/azure.txt'],
		['azure-gov', 'https://download.microsoft.com/download/6/4/D/64DB03BF-895B-4173-A8B1-BA4AD5D4DF22/ServiceTags_AzureGovernment_20200420.json', 'data/azure-gov.txt'],
	]

	for cloud in clouds:
		(provider, url, file) = cloud

		count += update_azure(provider, url, file)

	return count