import ipaddress
import socket

# https://ip-ranges.amazonaws.com/ip-ranges.json

def check(ips):
	if isinstance(ips, str):
		ips = [ips]

	# Initialize results
	results = []

	# Load json data
	with open("data/asns.txt", "r") as f:
		data = f.read().splitlines()
		f.close()

	# Loop each route
	for route in data:
		(cidr,provider,service,region) = route.split()

		# Loop each IP
		for ip in ips:
			if ipaddress.ip_address(ip) in ipaddress.ip_network(cidr):
				results.append({
					'ip': ip,
					'provider': provider,
					'service': service,
					'region': region
					})

	return results

def update():
	providers = {
		'alibaba': 'AS45102',
		'digitalocean': 'AS14061',
		'ibm': 'AS36351',
		'linode': 'AS63949',
		'rackspace': 'AS27357'
	}

	data = []

	for provider, asn in providers.items():
		routes = asn_routes(asn)

		for route in routes:
			data.append('%s %s unknown unknown' % (route, provider))

	with open('data/asns.txt', 'w') as f:
		f.write("\n".join(data))
		f.close()

def asn_routes(asn):
	host = 'whois.radb.net'
	port = 43

	routes = []

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))
	s.send(b"-i origin %s\n" % (asn.encode()))

	buffer = b''

	def process_line(line):
		if line[0:6] == b'route:' or line[0:7] == b'route6:':
			routes.append(line.split()[1].decode())

	while True:
		received = s.recv(1024)
		if len(received) == 0:
			break
		buffer += received

		while True:
			newline = buffer.find(b"\n")
			if newline == -1:
				break

			process_line(buffer[0:newline])
			buffer = buffer[newline+1:]

	process_line(buffer)

	s.close()

	return routes