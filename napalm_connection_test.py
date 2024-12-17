from napalm import get_network_driver

driver = get_network_driver("nxos_ssh")
device = driver("10.10.20.177", "cisco", "cisco")
device.open()
print("Successfully connected!")
print(device.get_facts())
device.close()