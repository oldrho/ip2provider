import ipaddress
import requests
import netaddr

# https://support.google.com/a/answer/10026322

GOOGLE_CLOUD_NETBLOCKS_URL = "https://www.gstatic.com/ipranges/cloud.json"
GOOGLE_ALL_NETBLOCKS_URL = "https://www.gstatic.com/ipranges/goog.json"

def update():
        results = []
        try:
                google_cloud_netblocks = []
                response_dict = requests.get(GOOGLE_CLOUD_NETBLOCKS_URL).json()
                for p in response_dict['prefixes']:
                        if 'ipv4Prefix' in p and 'scope' in p:
                                results.append("%s gcp GoogleCloudPlatform %s" % (p['ipv4Prefix'], p['scope']))
                                google_cloud_netblocks.append(p['ipv4Prefix'])

                google_all_netblocks = []
                response_dict = requests.get(GOOGLE_ALL_NETBLOCKS_URL).json()
                for p in response_dict['prefixes']:
                        if 'ipv4Prefix' in p:
                                google_all_netblocks.append(p['ipv4Prefix'])


                google_cloud_ipset = netaddr.IPSet(google_cloud_netblocks)
                for n in google_all_netblocks:
                        delta = netaddr.IPSet([n]) - google_cloud_ipset
                        #print(delta)
                        for c in delta.iter_cidrs():
                                results.append("%s gcp GoogleService unknown" % c)
                
        except Exception as e:
                #print(f'{e}')
                pass

        with open("data/gcp.txt", "w") as f:
                f.write("\n".join(results))
                f.close()

        return len(results)
