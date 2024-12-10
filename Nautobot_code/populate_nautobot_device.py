import requests
import json
import re
from netmiko import ConnectHandler
from ncclient import manager
from parser_utils import parse_interfaces, parse_running_config
from data_collection_utils import get_running_config, get_restconf_data, get_netconf_data
from nautobot_api_utils import create_or_update_in_nautobot, push_to_nautobot, get_device_id
from interface_utils import push_interfaces_to_nautobot, push_vlans_to_nautobot

# Device details for Cisco IOS-XR device
device = {
    "device_type": "cisco_ios",
    "host": "sbx-nxos-mgmt.cisco.com",
    "username": "admin",
    "password": "Admin_1234!",
}

token = "79c056180ba76e6e39b8cccf4b2ef9e635b15c15"

if __name__ == "__main__":
    # Choose the method to gather data: 'cli', 'restconf', or 'netconf'
    method = 'cli'  # Change this line to 'restconf' or 'netconf' as needed

    # Gather data based on the chosen method
    if method == 'cli':
        gathered_data = get_running_config(device)
        parsed_data = parse_running_config(gathered_data)
        device_name = "wee01-leaf-01"  # Ensure the name follows the defined naming standard
    elif method == 'restconf':
        gathered_data = get_restconf_data(device)
        parsed_data = gathered_data
        device_name = "wee01-leaf-01"
    elif method == 'netconf':
        gathered_data = get_netconf_data(device)
        parsed_data = gathered_data
        device_name = "wee01-leaf-01"
    else:
        raise ValueError("Invalid method chosen. Please select 'cli', 'restconf', or 'netconf'.")

    # Format data to push to Nautobot (this is just an example, adapt as needed)
    nautobot_data = {
        "name": device_name,
        "device_type": {"model": "Nexus-9Kv"},  # Update with an existing model in Nautobot
        "manufacturer": "Cisco",  # Manufacturer name must match what exists in Nautobot
        "role": {"name": "Router"},  # Must match an existing role in Nautobot
        "location": {"name": "Weehawken"},  # Must match an existing site in Nautobot
        "status": {"name": "active"},
        "serial": "123456",  # Example serial number, you can adapt as needed
    }

    # Push the gathered data to Nautobot
    push_to_nautobot(nautobot_data, token)

    # Push interface data to Nautobot
    if parsed_data and "interfaces" in parsed_data:
        device_id = get_device_id(device_name, token)
        if device_id:
            push_interfaces_to_nautobot(device_id, parsed_data["interfaces"], token)
        else:
            print("Device ID not found, unable to push interface data.")


    # Push VLAN data to Nautobot
    if parsed_data and "vlans" in parsed_data:
        device_id = get_device_id(device_name, token)
        if device_id:
            push_vlans_to_nautobot(device_id, parsed_data["vlans"], token=token)
        else:
            print("Device ID not found, unable to push VLAN data.")