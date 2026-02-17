#!/usr/bin/python3

""" 
Called by entryPoint.py, performs the addition or deletion of an item in a Cloudflare custom list.
Support for IPV6 is limited as it blocks the entire /64 subnet.

Change the following variables
- <user id> and <list id>, that can be found when creating the list
- <auth token>, that can be found when creating an API token
"""

import sys
import requests
from requests import Response
import json
import ipaddress

def getIPList(apiEndpoint : str, headers : dict) -> json:
    response = requests.get(apiEndpoint, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch existing IP list. Status code: {response.status_code}")
        print(response.text)
        sys.exit(1)

def addIPtoList(ipAddr : str, apiEndpoint : str, headers : dict) -> Response:
    payload = [{"ip": ipAddr}]
    response = requests.post(apiEndpoint, headers=headers, data=json.dumps(payload))
    return response

def removeIPFromList(ipId : str, apiEndpoint : str, headers : dict) -> Response:
    payload = {"items": [{"id": ipId}]}
    response = requests.delete(apiEndpoint, headers=headers, data=json.dumps(payload))
    return response

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./modifyBanList.py <ip> <add|del>")
        sys.exit(1)

    ipAddr = sys.argv[1]

    try:
        addr = ipaddress.IPv6Address(ipAddr)
        first_64_bits = str(addr.exploded).split(':')[:4]
        ipAddr = ':'.join(first_64_bits) + '::/64'
    except:
        pass

    action = sys.argv[2]
    listId = ''
    accountId = ''
    email = ''
    apiKey = ''
    apiEndpoint = f'https://api.cloudflare.com/client/v4/accounts/<user id>/configurations/lists/<list id>'

    headers = {
        'Authorization': f'Bearer <auth token>',
        'Content-Type': 'application/json'
    }

    existingIpList = getIPList(apiEndpoint,headers)
    print(existingIpList)
    response = None

    if action == "del":
        ipId = None
        for item in existingIpList['result']:
            try:
                # We have to convert to Python's IPv6 representation as Cloudflare remove leading zero (for instance), which messes up the comparaison
                item_ipAddr = item['ip']
                item_ipAddr = item_ipAddr.replace('/64', '')
                item_addr = ipaddress.IPv6Address(item_ipAddr)
                item_first_64_bits = str(item_addr.exploded).split(':')[:4]
                item_ipAddr = ':'.join(item_first_64_bits) + '::/64'
            except:
                # If it doesn't work, it's probably IPv4
                item_ipAddr = item['ip']
            if item_ipAddr == ipAddr:
                ipId = item['id']
                break
        payload = {"items": [{"id": ipId}]}

        if ipId is not None:
            response = requests.delete(apiEndpoint,headers=headers,data=json.dumps(payload))
    elif not any(item['ip'] == ipAddr for item in existingIpList['result']):
        payload = [{
            "ip": ipAddr
        }]
        response = requests.post(apiEndpoint, headers=headers, data=json.dumps(payload))

    if response is not None and response.status_code == 200:
            print(f"IP address {ipAddr} {action} to the custom IP list successfully.")
    else:
        print(f"Failed to {action} IP address {ipAddr} to the custom IP list.")
