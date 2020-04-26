import ipaddress

# DNS TXT _cloud-netblocks.googleusercontent.com

def check(ips):
	if isinstance(ips, str):
		ips = [ips]

	# Initialize results
	results = []

	# Load CIDR ranges
	with open("data/gcp.txt", "r") as f:
		data = f.read().splitlines()
		f.close()

	# Loop through each CIDR entry
	for cidr in data:
		# Loop through each IP
		for ip in ips:

			if ipaddress.ip_address(ip) in ipaddress.ip_network(cidr):
				results.append({
					'ip':ip,
					'provider':'gcp',
					'service':'GoogleCloudPlatform',
					'region':'unknown'
					})

	return results
