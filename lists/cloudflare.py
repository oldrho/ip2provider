import ipaddress
import requests

CLOUDFLARE_IP_URLS = [
    'https://www.cloudflare.com/ips-v4/',
    'https://www.cloudflare.com/ips-v6/',
    ]

def update():
    results = []

    for url in CLOUDFLARE_IP_URLS:
        response = requests.get(url)

        if response.status_code != 200:
            return False

        cidrs = response.text.splitlines()
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
