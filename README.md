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

**Flags**

* `-o`, `--output`: Select an output format (default `text`)
	`text` will output one result per line
	`json` will output a JSON array
	`raw` will output all results in a JSON array without filtering
* `--update-lists`: Update the route lists for each provider

## Notes

**Supported Providers**

* Microsoft Azure (Public and Government Clouds)
* Amazon Web Services (AWS)
* Oracle Cloud
