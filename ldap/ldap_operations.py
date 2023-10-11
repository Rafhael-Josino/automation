from ldap3 import Server, Connection, ALL, MODIFY_ADD, MODIFY_DELETE
from ldap_access import server_address, private_path

server = Server(server_address, get_info=ALL)
conn = Connection(server, auto_bind=True)
conn.start_tls()


def get_user(user_name):
	conn.search(
		private_path,
		'(&(objectclass=person)(uid={}))'.format(user_name),
		attributes=['uidNumber'],
	)

	return conn.entries


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
