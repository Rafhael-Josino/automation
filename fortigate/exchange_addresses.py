'''
Exchange addresses in groups and policies
'''

from colorama import init
from termcolor import colored

def exchange_addresses(fgt, exchanged, new_add):
	try:
		init()

		if fgt.address.is_exist(uid=exchanged) == False:
			raise Exception("Address", exchanged, "does not exists")
		if fgt.address.is_exist(uid=new_add) == False:
			raise Exception("Address", new_add, "does not exists")
		
		print('\n')
	
		# Check if address is in any group
		groups = fgt.address_group.get(filter="member=@" + exchanged)
		success_count = 0
		
		color = "green" if len(groups) == 0 else "red"
		print("Found address in", end=" ")
		print(colored(str(len(groups)) + " groups\n", color))
	
		for group in groups:
			print('>' + group["name"])
			new_members = list(filter(lambda member: member["name"] != exchanged, group["member"]))
			new_members.append({"name": new_add})
			fgt.address_group.update({"member": new_members}, group["name"])
			
		print(100 * '-', "\n")
	
	
		# Check if address is a source of any policies
		src_policies = fgt.policy.get(filter="srcaddr=@" + exchanged)
	
		color = "green" if len(src_policies) == 0 else "red"
		print("Found address in the source of", end=" ")
		print(colored(str(len(src_policies)) + " policies\n", color))
	
		for policy in src_policies:
			print('>' + policy["name"])
			new_src = list(filter(lambda src: src["name"] != exchanged, policy["srcaddr"]))
			new_src.append({"name": new_add})
			fgt.policy.update({"srcaddr": new_src}, policy["policyid"])
			
		print(100*'-', "\n")
	
		# Check if address is the destiny of any policies
		dst_policies = fgt.policy.get(filter="dstaddr=@" + exchanged)
	
		color = "green" if len(dst_policies) == 0 else "red"
		print("Found address in the destiny of", end=" ")
		print(colored(str(len(dst_policies)) + " policies\n", color))
	
		for policy in dst_policies:
			print('>' + policy["name"])
			new_dst = list(filter(lambda dst: dst["name"] != exchanged, policy["dstaddr"]))
			new_dst.append({"name": new_add})
			fgt.policy.update({"dstaddr": new_dst}, policy["policyid"])
	
		print(100*'-', "\n")
	
		fgt.address.delete(uid=exchanged)
		if fgt.address.is_exist(uid=exchanged) == False:
			print("Address", exchanged, "excluded with success")
			
	except Exception as e:
		print("Catch error\n", e.__str__())

	finally:
		print('\n')
