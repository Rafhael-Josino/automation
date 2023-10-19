def get_host_by_id(zapi, hostids):
	try:
		return zapi.host.get(
			hostids=hostids,
			output=["host", "hostid", "description"]
		)
	except Exception as e:
		print(e.__str__())


def get_host_by_group(zapi, groupids):
	try:
		return zapi.host.get(
			groupids=groupids,
			output=["host", "hostid", "description"]
		)
	except Exception as e:
		print(e.__str__())
