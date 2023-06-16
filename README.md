# Resume

This project consists in some solutions that aim to automate tasks from different environments. So far, the following ones are present:

- A network compost of Cisco routers and switches that uses Ansible to backup configurations and gather some informations like interfaces status, neighbors etc.

- A Fortigate firewall, where is used the Python library fortigate-api to create addresses objects in the firewall and add them to groups. The solution started using Ansible, creating groups of objects, but it was changed to the direct use of Python.

# TO DO

- To the firewall environment, create a script to discover the address which have the same subnet. In the Fortigate, an address entity can be associated to a subnet (from a single IP to any network size), as it can also translate to the real world as a MAC address or a domain name. Therefore, it is possible to hava multiple address objects with the same subnets (just imagine people who do not talk to each other meddling with the firewall and creating the same networks in different objects).

- Extend the project to a Zabbix server using py-zabbix.

- In the network environment, create playbooks with Dell modules.
