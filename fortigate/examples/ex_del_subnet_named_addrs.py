'''
This script search for all subnets that are present in more than one address

In the case of one of those addresses's name is a subnet itself, it will be
substituted by the other address and then deleted
'''

from fortigate_api import FortigateAPI
import socket
import fgt_access
from exchange_addresses import exchange_addresses
from get_repeated_addresses import get_repeated_addresses

fgt = FortigateAPI(host=fgt_access.fgt_address, token=fgt_access.fgt_token)

(subnets, repeated_subnets) = get_repeated_addresses(fgt)
# subnets -> dict -> subnet: address.name[]
# repeated_subnets -> subnet_string[]

for subnet in repeated_subnets:
	# Verifiy wether the first (change to any) address name is an IP
	# Those one shall be all exchanged for the next address in the list

	to_delete = None
	to_substitute = None

	# For each address that has the same subnet:
	for address in subnets[subnet]:
		try:
			# If the address name is a subnet itself
			socket.inet_aton(address)
			to_delete = address
		except:
			try:
				# In the case of the name has the mask at it end
				# Example: 192.168.0.0/16
				socket.inet_aton(address[:-3])
				to_delete = address
			except:
				try:
					# Example: 10.0.0.0/8
					socket.inet_aton(address[:-2])
					to_delete = address
				except:
					to_substitute = address

	exchange_addresses(fgt, to_delete, to_substitute)
