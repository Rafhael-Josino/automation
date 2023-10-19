from ldap3 import Server, Connection, ALL, MODIFY_ADD, MODIFY_DELETE
from ldap_access import server_address, ldap_credentials, private_path

server = Server(server_address, get_info=ALL)
conn = Connection(server, ldap_credentials["login"], ldap_credentials["password"], auto_bind=True)


def get_user(user_name, attributes=[]):
	conn.search(
		private_path,
		'(&(objectclass=person)(uid={}))'.format(user_name),
		attributes=attributes,
	)

	return conn.entries


def list_groups(detail=False):
	conn.search(
		"ou=groups,{}".format(private_path),
		"(cn=*)",
		attributes=['description', 'cn', 'memberUid']
	)

	for group in conn.entries:
		if detail:
			print(
				group.cn,
				"\tDescription: {}".format(group.description),
				"\tTotal members: {}\n".format(len(group.memberUid)),
				sep="\n"
			)	
		else:
			print(group.cn, group.description)


def get_users_from_group(group_name):
	conn.search(
		"ou=groups,{}".format(private_path),
		'(cn={})'.format(group_name),
		attributes=['memberUid']
	)

	return conn.entries[0].memberUid


def check_user_in_group(user_name, group_name):
	user = "uid={},ou=People,{}".format(user_name, private_path)

	if user in get_users_from_group(group_name):
		return True

	else:
		return False


def add_user_to_group(user_name, group_name):
	conn.modify(
		"cn={},ou=groups,{}".format(group_name, private_path),
		{ "memberUid": [( MODIFY_ADD, ["uid={},ou=People,{}".format(user_name, private_path)] )] },
	)


def del_user_from_group(user_name, group_name):
	conn.modify(
		"cn={},ou=groups,{}".format(group_name, private_path),
		{ "memberUid": [( MODIFY_DELETE, ["uid={},ou=People,{}".format(user_name, private_path)] )] },
	)
