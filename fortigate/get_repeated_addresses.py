'''
Get all addresses that have repeated values of subnets ###
'''

def get_repeated_addresses(fgt):
	addresses = fgt.address.get()
	
	subnets = {}
	
	for address in addresses:
		# Gets addresses that are only of the type "subnet"
		try:
			if address["subnet"] in subnets.keys():
				subnets[address["subnet"]].append(address["name"])
			else:
				subnets[address["subnet"]] = [address["name"]]
		except:
			pass  
	
	repeated_subnets = list(filter(lambda subnet: len(subnets[subnet]) > 1, subnets.keys()))

	return (subnets, repeated_subnets)
