# ip2provider

Check which cloud provider is hosting a particular IP address. Some providers will also have service and region listed

```
./ip2provider [flags] <ip>
```

## Installation

**TODO**

## Usage

**Flags**

* `-o`, `--output`: Select an output format (default `text`)
	`text` will output one result per line
	`json` will output a JSON array
	`raw` will output all results in a JSON array without filtering

## Notes

**Supported Providers**

* Microsoft Azure (Public and Government Clouds)
* Amazon Web Services (AWS)
* Oracle Cloud