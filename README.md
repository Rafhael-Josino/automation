# Resume

This project consists in some solutions that aim to automate tasks from different environments. So far, the following ones are present:

- A network compost of Cisco routers and switches that uses Ansible to backup configurations and gather some informations like interfaces status, neighbors etc.

- A Fortigate firewall, where is used the Python library fortigate-api to create addresses objects in the firewall and add them to groups. The solution started using Ansible, creating groups of objects, but it was changed to the direct use of Python.

# TO DO

- In the network environment, create playbooks with Dell modules.