import ipaddress
import json
import requests
import re

AZURE_CONFIRMATION_URL = "https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519"
AZURE_DEFAULT_URL = "https://download.microsoft.com/download/7/1/D/71D86715-5596-4529-9B13-DA13A5DE5B63/ServiceTags_Public_20231113.json"
AZURE_GOV_CONFIRMATION_URL = "https://www.microsoft.com/en-us/download/confirmation.aspx?id=57063"
AZURE_GOV_DEFAULT_URL = "https://download.microsoft.com/download/6/4/D/64DB03BF-895B-4173-A8B1-BA4AD5D4DF22/ServiceTags_AzureGovernment_20231113.json"
AZURE_DOWNLOAD_REGEX = r'https://download\.microsoft\.com.*?\.json'
AZURE_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'

def get_latest_download_url(confirmation_url, regex, default_download_url):
        try:
                r = requests.get(confirmation_url, headers={'User-Agent': AZURE_USER_AGENT})
                if r.status_code == 200:
                        match = re.search(regex, r.text)
                        if match:
                                ret = match.group(0)
                                return ret
                        
        except Exception as e:
                pass

        return default_download_url

def update():

	def update_azure(provider, url, file):
		results = []
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
		[
			'azure',
			get_latest_download_url(
				AZURE_CONFIRMATION_URL,
				AZURE_DOWNLOAD_REGEX,
				AZURE_DEFAULT_URL
				),
			'data/azure.txt'
			],
		[
			'azure-gov',
			get_latest_download_url(
				AZURE_GOV_CONFIRMATION_URL,
				AZURE_DOWNLOAD_REGEX,
				AZURE_GOV_DEFAULT_URL
				),
			'data/azure-gov.txt',
			],
	]

	for cloud in clouds:
		(provider, url, file) = cloud
		count += update_azure(provider, url, file)

	return count
