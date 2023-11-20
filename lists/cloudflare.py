import ipaddress
import requests
from bs4 import BeautifulSoup as bs

# https://www.cloudflare.com/en-ca/ips/
# Texts lists 404, must be scraped

def update():
	results = []
	urls = [
		'https://www.cloudflare.com/ips-v4/',
		'https://www.cloudflare.com/ips-v6/',
		]

	for url in urls:
		response = requests.get(url)

		if response.status_code != 200:
			return False

		cidrs = response.text.split('\n')
		for cidr in cidrs:
			try:
				ipaddress.ip_network(cidr)
			except:
				continue

			results.append("%s %s unknown unknown" % (cidr, 'cloudflare'))

	# Write results to file
	with open('data/cloudflare.txt', 'w') as f:
		f.write("\n".join(results))
		f.close()

	return len(results)
