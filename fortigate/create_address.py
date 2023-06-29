'''
Registers an address in the Fortigate and, if the third argument was passed
adds it to the specified group address
In the case that the new address's subnet already is registered under an existing
address, a warning is printed and the first of such addresses (it can be one or more)
is added to the group (if specified)
'''

from colorama import init
from termcolor import colored

def create_address(fgt, name, ip, mask=None, group_name=None):
	init()
	subnet = ip + " " + (mask if mask else "255.255.255.255")

	# Checking if an address of same name already exists
	if fgt.address.is_exist(uid=name):
		print(colored("There is already an address with this name", "red"))
		return None

	# Checking if an address with this IP already exists
	address_search = fgt.address.get(filter = ("subnet=@" + subnet))

	if len(address_search):
		print("There are already", len(address_search), "address(es) with the subnet:\n{}".format(subnet))
		for address in address_search:
			print(">{}".format( address["name"]))
		print(colored("The address was not added".format(name), "red"))

		if group_name:
			name = address_search[0]["name"]
			print("The address {} will be added then to the group {}".format(name, group_name))

	else:
		# Creating new address
		data = {"name": name,
			"obj-type": "ip",
			"subnet": subnet,
			"type": "ipmask"}

		fgt.address.create(data)
		
		print(colored("Created the following address:", "green"))
		print("Name:", name)
		print("Subnet:", subnet)

	if group_name:
		# Adding the first address found to the specified group
		group = fgt.address_group.get(uid=group_name)[0]
		members = group["member"]
		members.append({"name": name})
		fgt.address_group.update({"member": members}, group_name)
		print("Address", name, "added to", group_name)
