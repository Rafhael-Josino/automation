import yaml

def get_host(zapi, host_name):
	try:
		return zapi.host.get(
			filter={"host": host_name},
			output=["host", "hostid", "description", "template"],
			# Versao 5
			#selectParentTemplates=["id", "name"],
			# Versao 6
			selectParentTemplates=["templateid", "name"],
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


def add_host(zapi, name, ip, community, description, groups, templates):
	try:
		if len(get_host(zapi, name)) > 0:
			print("Host {} already exists".format(name))
			return False
		
		else:
			new_host = zapi.host.create(
				host=name,
				status=0,
				interfaces=[
					{
						"type": 1,
						"main": 1,
						"useip": 1,
						"ip": ip,
						"dns": "",
						"port": "10050",
					},	
					{
						"type": 2,
						"main": 1,
						"useip": 1,
						"ip": ip,
						"dns": "",
						"port": "161",
						"details": {
							"version": 2,
							"community": community,
						},
					},
				],
				description=description,
				groups=groups,
				templates=templates,
			)

		print("Host", name, "id:", new_host, "created with success")
		return new_host
	
	except Exception as e:
		print("Error at creating host", name)
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
