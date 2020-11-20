import ipaddress
import requests
from bs4 import BeautifulSoup as bs

# https://www.cloudflare.com/en-ca/ips/
# Texts lists 404, must be scraped

def update():
	results = []

	response = requests.get('https://www.cloudflare.com/en-ca/ips/')

	if response.status_code != 200:
		return False

	soup = bs(response.text, features='html.parser')
	elements = soup.find('h2',string='IPv4').parent.find_all('li')

	for elem in elements:
		cidr = elem.text
		results.append("%s %s unknown unknown" % (cidr, 'cloudflare'))

	# Write results to file
	with open('data/cloudflare.txt', 'w') as f:
		f.write("\n".join(results))
		f.close()

	return len(results)
