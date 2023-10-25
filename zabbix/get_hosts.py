import yaml

def get_host(zapi, host_name):
	try:
		return zapi.host.get(
			filter={"host": host_name},
			output=["host", "hostid", "description", "template"],
			selectParentTemplates=["id", "name"],
			selectInterfaces=["ip"]
		)
	except Exception as e:
		print(e.__str__())


def get_host_by_group(zapi, group_id):
	try:
		return zapi.host.get(
			groupids=group_id,
			output=["host", "description"],
			selectParentTemplates=["id", "name"],
			# For version 5:
			selectGroups=["groupid", "name"],
			###
			selectInterfaces=["ip"]
		)
	except Exception as e:
		print(e.__str__())


def create_hosts_inventory(zapi, inventory_vars=[]):
	hosts_obj = {
		"all": {
			"hosts": None,
			"children": {},
		}
	}

	for inventory in inventory_vars:
		group_name = zapi.hostgroup.get(groupids=inventory[0], output="extend")[0]["name"]

		hosts_obj["all"]["children"][group_name] = {
			"hosts": {},
			"vars": inventory[1]
		}

		hosts_from_group = get_host_by_group(zapi, inventory[0])

		for zabbix_host in hosts_from_group:
			hosts_obj["all"]["children"][group_name]["hosts"][zabbix_host["host"]] = {
				"ansible_host": zabbix_host["interfaces"][0]["ip"],
				"name": zabbix_host["host"]
			}
		
	with open("hosts.yaml", "w") as file:
		yaml.dump(hosts_obj, file)	
