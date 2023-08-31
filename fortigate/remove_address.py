'''
Remove address from a group
If desired so, the address will be deleted (if it is no longer in use)
'''

from colorama import init
from termcolor import colored

def remove_addr_by_name(fgt, address, group=None, policy=None, delete=False):
	init()

	if fgt.address.is_exist(uid=address) == False:
		print(colored("Address {} does not exist".format(address)), "red")
		return None

	if group:
		fgt_group = fgt.address_group.get(uid=group)[0]
		new_members = list(filter(lambda member: member["name"] != address, fgt_group["member"]))
		fgt.address_group.update({"member": new_members}, group)
		print(colored("{} removed from group {}".format(address, group), "green"))

	if policy:
		pass

	if delete:
		print("Trying to delete address {}".format(address))

		# Trying to delete the address
		fgt.address.delete(uid=address)

		# Checking wether it was deleted
		if fgt.address.is_exist(uid=address) == False:
			print("Address {}".format(address), colored("deleted with success", "green"))
		else:
			print("Address {}".format(address), colored("could not be deleted", "red"))

	else:
		print("Address {} removed from inputs but opted for no deletion".format(address))



def remove_addr_by_subnet(fgt, subnet, group=None, policy=None, delete=False):
	init()

	address_search = fgt.address.get(filter = ("subnet=@" + subnet))

	if len(address_search) == 0:
		print(colored("Address {} does not exist".format(subnet), "red"))
		return None

	elif len(address_search) > 1:
		print(colored("There are {} address with this subnet!".format(subnet), "red"))
		return None

	address = address_search[0]["name"]

	if group:
		fgt_group = fgt.address_group.get(uid=group)[0]
		new_members = list(filter(lambda member: member["name"] != address, fgt_group["member"]))
		fgt.address_group.update({"member": new_members}, group)
		print(colored("{} removed from group {}".format(address, group), "green"))

	if policy:
		pass

	if delete:
		print("Trying to delete address {}".format(address))

		# Trying to delete the address
		fgt.address.delete(uid=address)

		# Checking wether it was deleted
		if fgt.address.is_exist(uid=address) == False:
			print("Address {}".format(address), colored("deleted with success", "green"))
		else:
			print("Address {}".format(address), colored("could not be deleted", "red"))

	else:
		print("Address {} removed from inputs but opted for no deletion".format(address))
