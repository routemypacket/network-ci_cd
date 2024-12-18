from napalm import get_network_driver

driver = get_network_driver("nxos_ssh")
device = driver("131.226.217.151", "admin", "131.226.217.151")
device.open()
print("Successfully connected!")
print(device.get_facts())
device.close()