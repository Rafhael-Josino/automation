from colorama import init
from termcolor import colored


def find_ref(fgt, ip, mask=None):
	print(100*'-', "\n")
	init()
	subnet = ip + " " + (mask if mask else "255.255.255.255")
	
	address_search = fgt.address.get(filter = ("subnet=@" + subnet))

	if len(address_search) == 0:
		print("There is no addresses with this subnet")
		return None


	if len(address_search) > 1:
		print(colored("There are {} repeated addresses with the same subnet".format(len(address)), "red"))

		i=1
		for address in address_search:
			print("{} > {}".format(i, address["name"]))
		
		return None


	print("One address found:", end=" ")
	print(colored(address_search[0]["name"]+"\n", "green"))

	print(100*'-', "\n")

	groups = fgt.address_group.get(filter="member=@"+address_search[0]["name"])
	
	print("Found address in", end=" ")
	print(colored(str(len(groups)) + " groups\n", "green"))

	for group in groups:
		print('>' + group["name"])

	print(100*'-', "\n")

	# Check if address is a source of any policies
	src_policies = fgt.policy.get(filter="srcaddr=@"+address_search[0]["name"])

	print("Found address in the source of", end=" ")
	print(colored(str(len(src_policies)) + " policies\n", "green"))

	for policy in src_policies:
		print('>' + policy["name"])

	print(100*'-', "\n")

	# Check if address is the destiny of any policies
	dst_policies = fgt.policy.get(filter="dstaddr=@"+address_search[0]["name"])

	print("Found address in the destiny of", end=" ")
	print(colored(str(len(dst_policies)) + " policies\n", "green"))

	for policy in dst_policies:
		print('>' + policy["name"])
	
	print(100*'-', "\n")
