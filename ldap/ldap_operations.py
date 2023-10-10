from ldap3 import Server, Connection, ALL
from ldap_access import server_address, private_user_dn

server = Server(server_address, get_info=ALL)
conn = Connection(server, auto_bind=True)
conn.start_tls()


def get_user(user_name):
	conn.search(
		"dc=21ct,dc=eb,dc=mil,dc=br",
		'(&(objectclass=person)(uid={}))'.format(user_name),
		attributes=['uidNumber'],
	)

	return conn.entries[0]


def get_users_from_group(group_name):
	conn.search(
		"ou=groups,dc=21ct,dc=eb,dc=mil,dc=br",
		'(cn={})'.format(group_name),
		attributes=['memberUid']
	)

	return conn.entries[0].memberUid


def check_user_in_group(user_name, group_name):
	'''private_user_dn() returns the user's dn according to the costumer's ldap structure'''
	if private_user_dn(user_name) in get_users_from_group(group_name):
		return True
	else:
		return False
