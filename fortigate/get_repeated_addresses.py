from fortigate_api import FortigateAPI
import fgt_access

fgt = FortigateAPI(host=fgt_access.fgt_address, token=fgt_access.fgt_token)


##############################################################
### Get all addresses that have repeated values of subnets ###
##############################################################

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

print(len(repeated_subnets), "repeated addresses found")
for subnet in repeated_subnets:
	print(subnet, "\n\t", subnets[subnet])
