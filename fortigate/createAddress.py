from fortigate_api import FortigateAPI
from sys import argv
import fgt_access

#######################################################################################

# Registers an address in the Fortigate and, if the third argument was passed
# adds it to the specified group address
# In the case that the new address's subnet already is registered under an existing
# address, a warning is printed and the first of such addresses (it can be one or more)
# is added to the group (if specified)

# Arguments:
# argv[1] -> New address's subnet
# argv[2] -> New address's name 
# argv[3] -> Group where the new address will be added (optional)

#######################################################################################


fgt = FortigateAPI(host=fgt_access.fgt_address, token=fgt_access.fgt_token)

if len(argv) < 3:
	print("The command lacks arguments")
else:
	# Checking if an address with this IP already exists
	address_search = fgt.address.get(filter = ("subnet=@" + argv[1]))

	if len(address_search):
		print("There are already", len(address_search), "address(es) with the subnet", argv[1])

		if len(argv) == 4:
			# Adding the first address found to the specified group
			group = fgt.address_group.get(uid=argv[3])[0]
			members = group["member"]
			members.append({"name": address_search[0]["name"]})
			fgt.address_group.update({"member": members}, group["name"])
			print("Address", address_search[0]["name"], "added to", group["name"])

	else:
		# Creating new address
		data = {"name": argv[2],
			"obj-type": "ip",
			"subnet": argv[1] +  " 255.255.255.255",
			"type": "ipmask"}

		fgt.address.create(data)
		print("Criado endereço", argv[2], "de IP", argv[1])

		if len(argv) == 4:
			# Adding new address to specified group
			group = fgt.address_group.get(uid=argv[3])[0]
			members = group["member"]
			members.append({"name": argv[2]})
			fgt.address_group.update({"member": members}, group["name"])
			print("Endereço", argv[2], "adicionado ao grupo", argv[3])
