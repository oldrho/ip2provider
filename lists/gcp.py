import ipaddress

def check(ips):
	if isinstance(ips, str):
		ips = [ips]
