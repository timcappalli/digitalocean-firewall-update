# DigitalOcean Firewall Update

![version 2018.01](https://img.shields.io/badge/Version-2018.01-brightgreen.svg "version 2018.01") [![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/Apache-2.0)


## Overview
This Python script will add an inbound rule to DigitalOcean firewall. An IP address (v4 or v6) can be passed to the script or the local machine's public IPv4 and/or IPv6 address can be detected and passed to the script.

## Current Version
2018.01 (2018-11-12)

## Dependencies
* DigitalOcean tenant with existing firewall
* DigitalOcean API key
* Python 3
* Modules: `requests, json, os, configparser, argparse`

## Configuration
The configuration file is config.cfg
### Required
* do_token = the DigitalOcean API access token (https://cloud.digitalocean.com/account/api/tokens)
* firewall_id = the ID of the firewall object. This GUID can be found in the URL after clicking on the firewall (https://cloud.digitalocean.com/networking/firewalls)


## Usage

> `python3 update_firewall.py <tcp|udp|icmp> <port|range|all> <me|ipaddr>`

Passing 'me' instead of an IP address as the third parameter will auto detect the IPv4 and/or IPv6 address(es) of the local machine and use it as the source address the firewall rule.


## License and Other Information
This repo is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

Author: @timcappalli