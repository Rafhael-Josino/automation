from colorama import init
from termcolor import colored


def detail_refs(fgt, name):
	print("Address found:", end=" ")
	print(colored(name + "\n", "green"))

	print(100*'-', "\n")

	# Check if address is present in any group
	groups = fgt.address_group.get(filter="member=@" + name)
	
	print("Address found in:", end=" ")
	print(colored(str(len(groups)) + " grupos\n", "green"))

	for group in groups:
		print('>' + group["name"])

	print(100*'-', "\n")

	# Check if address is a source of any policies
	src_policies = fgt.policy.get(filter = "srcaddr=@" + name)

	print("Address found in the origin of", end=" ")
	print(colored(str(len(src_policies)) + " policies\n", "green"))

	for policy in src_policies:
		print('>' + policy["name"])

	print(100*'-', "\n")

	# Check if address is the destiny of any policies
	dst_policies = fgt.policy.get(filter = "dstaddr=@" + name)

	print("Address found in the destiny of", end=" ")
	print(colored(str(len(dst_policies)) + " policies\n", "green"))

	for policy in dst_policies:
		print('>' + policy["name"])
	
	print(100*'-', "\n")


def find_ref(fgt, ip, mask=None):
	print(100*'-', "\n")
	init()
	subnet = ip + " " + (mask if mask else "255.255.255.255")
	
	address_search = fgt.address.get(filter = ("subnet=@" + subnet))

	if len(address_search) == 0:
		print("There are no address with this IP")
		return None


	if len(address_search) > 1:
		print(colored("There are {} addresses with the same subnet".format(len(address_search)), "red"))

		loop = True
		while loop:
			i=1
			for address in address_search:
				print("{} > {}".format(i, address["name"]))
				i += 1
		
			print(i, "- LEAVE")

			option = int(input("Option: "))
			
			if option < i and option:
				detail_refs(fgt, address_search[option-1]["name"]) 

			else:
				loop = False

		print(100*'-', "\n")
		return None

	detail_refs(fgt, address_search[0]["name"])
