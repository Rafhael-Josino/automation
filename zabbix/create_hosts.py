from sys import argv
from pyzabbix.api import ZabbixAPI
import zabbixAccess
import groups_and_templates

##################################################
# Create a host with the following parameters
#
# argv[1] -> Host name
# argv[2] -> Host IP
# argv[3] -> Description
# 
# groups_and_templates.groups -> List of groups that the new host belongs
# groups_and_templates.templates -> List of templates that the new host has
#
##################################################


zapi = ZabbixAPI(url=zabbixAccess.url, user=zabbixAccess.user, password=zabbixAccess.password)

# Getting the IDs of the groups and templates imported (both are arrays of names)
groups = list(map(lambda name: {"groupid": zapi.get_id(item_type="hostgroup", item=name)}, groups_and_templates.groups))
templates  = list(map(lambda name: {"templateid": zapi.get_id(item_type="template", item=name)}, groups_and_templates.templates))

# Creating new host
new_host = zapi.host.create(
	host = argv[1],
	status = 0,
	interfaces = [{
		"type": 1,
		"main": "1",
		"useip": 1,
		"ip": argv[2],
		"dns": "",
		"port": 10050
	}],
	groups = groups,
	templates = templates,
	description= argv[3]
)


print("Host", argv[1], "id:", new_host, "created with success")
