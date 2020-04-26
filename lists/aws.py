import ipaddress
import json

def check(ips):
	if isinstance(ips, str):
		ips = [ips]

	# Initialize results
	results = []

	# Load json data
	with open("data/aws.json", "r") as f:
		data = json.loads(f.read())
		f.close()

	def loop_ips(group):
		# Loop through each IP
		for ip in ips:
			cidr = group['ip_prefix'] if 'ip_prefix' in group.keys() else group['ipv6_prefix']
			if ipaddress.ip_address(ip) in ipaddress.ip_network(cidr):
				results.append({
					'ip': ip,
					'provider':'aws',
					'service':group['service'],
					'region':group['region']
					})

	# Loop through all services
	for group in data['prefixes']:
		loop_ips(group)
	for group in data['ipv6_prefixes']:
		loop_ips(group)

	return results