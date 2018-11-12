#!/usr/bin/env python3

#------------------------------------------------------------------------------
#
# Author: @timcappalli
#
# Version: 2018.01
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#------------------------------------------------------------------------------

__version__ = "2018.01"


import json
import requests
import os
import argparse
from configparser import ConfigParser


def get_public_ipv4():

    url = 'https://ipv4.wtfismyip.com/json'

    try:
        r = requests.get(url)
        r.raise_for_status()
        result = r.json()

        return result['YourFuckingIPAddress']

    except Exception as e:
        error = r.json()

        print(e)
        exit(1)


def get_public_ipv6():

    url = 'https://ipv6.wtfismyip.com/json'

    try:
        r = requests.get(url)
        r.raise_for_status()
        result = r.json()
        return result['YourFuckingIPAddress']

    except Exception as e:
        error = r.json()

        print(e)
        exit(1)


def add_inbound_rule(do_token, firewall_id, port, protocol, source_address):

    url = "https://api.digitalocean.com/v2/firewalls/{}/rules".format(firewall_id)

    headers = {
        'Authorization': 'Bearer {}'.format(do_token),
        'content-type': "application/json"
    }

    body = {"inbound_rules": [{"protocol": protocol, "ports": port, "sources": {"addresses": source_address}}]}

    try:
        r = requests.post(url, headers=headers, data=json.dumps(body))
        r.raise_for_status()

        if r.status_code == 204:
            print("\nSuccessfully added firewall entry! \n\n\tpermit {}/{} from {}\n".format(protocol, port, source_address))

    except Exception as e:
        error = r.json()
        print(e)
        exit(1)


if __name__ == '__main__':

    config_file = os.path.join(os.path.dirname(__file__), "config-dev.cfg")
    config = ConfigParser()
    config.read(config_file)

    do_token = config.get('DigitalOcean', 'do_token')
    firewall_id = config.get('DigitalOcean', 'firewall_id')

    if not do_token:
        print('DigitalOcean access token required in config.cfg file.')
        exit(1)
    if not firewall_id:
        print('DigitalOcean Firewall ID required in config.cfg file.')
        exit(1)

    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("protocol", help="Protocol (TCP, UDP)")
    parser.add_argument("port", help="Port number")
    parser.add_argument("address", help="Source IP Address")
    args = parser.parse_args()

    port = args.port
    protocol = args.protocol
    address = args.address

    if address != "me":
        source_address = [address]
        add_inbound_rule(do_token, firewall_id, port, protocol, source_address)
        exit(0)

    if address == "me":
        ipv4_addr = get_public_ipv4()
        ipv6_addr = get_public_ipv6()

        if ipv4_addr and ipv6_addr:
            source_address = [ipv4_addr, ipv6_addr]
            add_inbound_rule(do_token, firewall_id, port, protocol, source_address)
            exit(0)
        elif ipv4_addr and not ipv6_addr:
            source_address = [ipv4_addr]
            add_inbound_rule(do_token, firewall_id, port, protocol, source_address)
            exit(0)
        elif ipv6_addr and not ipv4_addr:
            source_address = [ipv6_addr]
            add_inbound_rule(do_token, firewall_id, port, protocol, source_address)
            exit(0)
        else:
            print('No public IP address detected.')
            exit(1)
    else:
        print('No public IP address detected.')
        exit(1)
