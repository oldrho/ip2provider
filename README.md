# ip2provider

Check which cloud provider is hosting a particular IP address. Some providers will also have service and region listed

```
./ip2provider.py [flags] [ip]
```

## Installation

```
git clone https://github.com/oldrho/ip2provider.git
cd ip2provider
pip3 install -r requirements.txt
```

## Usage

**Arguments**

* `ip`: One or more comma-separated IP addresses

**Flags**

* `-o`, `--output`: Select an output format (default `text`)
	`text` will output one result per line
	`json` will output a JSON array
	`raw` will output all results in a JSON array without filtering
* `--update-lists`: Update the route lists for each provider

**Piped**

```
cat ip_addresses.txt | ./ip2provider.py
```
One IP address per line

## Notes

**Supported Providers**

* Amazon Web Services (AWS)
* Microsoft Azure (Public and Government Clouds)
* Google Cloud Platform (GCP)
* IBM/SoftLayer Cloud
* Oracle Cloud
* Alibaba Cloud
* Linode
* DigitalOcean

