import requests

CLOUDFLARE_IPV4_URL = "https://www.cloudflare.com/ips-v4"

def update():
        results = []
        r = requests.get(CLOUDFLARE_IPV4_URL)
        if r.status_code != 200:
                return False

        for cidr in r.text.splitlines():
                results.append("%s %s unknown unknown" % (cidr, 'cloudflare'))

        with open('data/cloudflare.txt', 'w') as f:
                f.write('\n'.join(results))
                f.close()

        return len(results)
