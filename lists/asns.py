import ipaddress
import socket

def update():
	providers = [
		['alibaba', 'AS45102', 'data/alibaba.txt'],
		['digitalocean', 'AS14061', 'data/digitalocean.txt'],
		['ibm', 'AS36351', 'data/ibm.txt'],
		['linode', 'AS63949', 'data/linode.txt'],
		['rackspace', 'AS27357', 'data/rackspace.txt']
	]

	total = 0

	for row in providers:
		(provider, asn, file) = row
		data = []
		
		routes = asn_routes(asn)

		for route in routes:
			data.append('%s %s unknown unknown' % (route, provider))

		total += len(data)
		with open(file, 'w') as f:
			f.write("\n".join(data))
			f.close()

	return total



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