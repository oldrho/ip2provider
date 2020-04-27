import ipaddress
import dns.resolver

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
	for entry in data:
		(cidr, provider, service, region) = entry.split()
		# Loop through each IP
		for ip in ips:

			if ipaddress.ip_address(ip) in ipaddress.ip_network(cidr):
				results.append({
					'ip':ip,
					'provider': provider,
					'service': service,
					'region': region
					})

	return results



def update():
	results = []
	service = ''



	def get_netblocks(hostname):
		nonlocal results, service

		query_results = dns.resolver.query(hostname, 'TXT')

		for query_result in query_results:
			line = query_result.to_text()

			if line.split()[0] != '"v=spf1':
				continue

			entries = line.split()[1:-1]

			for entry in entries:
				entry_type = entry.split(':')[0]
				address = ":".join(entry.split(':')[1:])

				if entry_type == 'include':
					get_netblocks(address)

				if entry_type == 'ip4' or entry_type == 'ip6':
					results.append("%s gcp %s unknown" % (address, service))

	# Google Cloud Platform
	service = 'GoogleCloudPlatform'
	get_netblocks("_cloud-netblocks.googleusercontent.com")

	# Google Services
	service = 'GoogleService'
	get_netblocks("_spf.google.com")



	# Write to file
	with open("data/gcp.txt", "w") as f:
		f.write("\n".join(results))
		f.close()

	return len(results)
