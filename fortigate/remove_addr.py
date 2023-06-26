'''
Remove address from a group
If desired so, the address will be delete if possible
'''

from colorama import init
from termcolor import colored

def remove_addr(fgt, address, group=None, policy=None, delete=False):
	try:
		init()

		if fgt.address.is_exist(uid=address) == False:
			raise ValueError("Address {} does not exist".format(address))

		if policy == None:
			fgt_group = fgt.address_group.get(uid=group)[0]
			new_members = list(filter(lambda member: member["name"] != address, fgt_group["member"]))
			fgt.address_group.update({"member": new_members}, group)

		if delete:
			print("Deleting the address {}".format(address))

			# Trying to delete the address
			fgt.address.delete(uid=address)
	
			# Checking wether it was deleted
			if fgt.address.is_exist(uid=address) == False:
				print("Address {}".format(address), colored("deleted with success", "green"))
			else:
				print("Address {}".format(address), colored("could not be deleted", "red"))

		else:
			print("Address {} removed from inputs but opted for no deletion".format(address))
	except Exception as e:
		print(colored("Error:\n{}".format(e.__str__()), "red"))
