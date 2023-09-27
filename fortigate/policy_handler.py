from termcolor import colored
from colorama import init

init()


'''Adds or exchanges source/destination of a policy'''
def exchange_intf(fgt, policyid, old_intf, new_intf, intf='srcintf', del_old=False):
	policy = fgt.policy.get(filter="policyid==" + str(policyid))

	if del_old:
		interfaces = list(filter(lambda intf: intf["name"] != old_intf, policy[0][intf]))
	else:
		interfaces = policy[0][intf]

	interfaces.append({"name": new_intf, "q_origin_key": new_intf})

	print(interfaces)

	if intf='srcintf':
		new_data = {
			"srcintf": interfaces
		}
	elif intf='dstintf':
		new_data = {
			"dstintf": interfaces
		}
	else:
		print("Bad input for parameter: intf")
		return None

	fgt.policy.update(new_data, policyid)


'''Get policies filtering by source/destination'''
def get_policies(fgt, old_intf, new_intf=None, intf='srcintf', del_old=False):

	policies = fgt.policy.get(filter=intf+"=@"+old_intf)

	if new_intf:
		for policy in policies:
			print(str(policy["policyid"]) + " - " + policy["name"])
			
			option = input("Exchange interface {} by {}? (Y/n)".format(old_intf, new_intf))

			if option == 'Y':
				exchange_intf(fgt, policy["policyid"], old_intf, new_intf, intf, del_old)
			elif option == 'n':
				print("Policy not modified")
			else:
				print("Invalid input - program terminated")
				break

	else:
		for policy in policies:
			print(str(policy["policyid"]) + " - " + policy["name"])
