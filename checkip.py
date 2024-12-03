import os

from netmiko import ConnectHandler

user = os.environ["USER"]
password = os.environ["PASSWORD"]

iosv_l2_s1 = {
    "device_type": "cisco_ios",
    "ip": "sandbox-iosxr-1.cisco.com test",
    "username": user,
    "password": password,
}

net_connect = ConnectHandler(**iosv_l2_s1)
output = net_connect.send_command("show ip int brief")
print(output)
