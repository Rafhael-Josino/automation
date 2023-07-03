'''
Adds elements in a map with the hosts passed in a box whose
dimentions are also passed as parameters

- (x0,y0) is the initial point where the first element will be inserted
- width represents the multiple of spacement that will constitute the actual
width of the box.
	For example, a width of 3 means that the box will have 3 elements of width
- height is the same thing but in the other dimension. This parameter and width
are both mutually excludents
'''

def add_element(zapi, sysmapid, hosts, iconid, x0, y0, spacement, width=None, height=None, counter=0):
	limit = (width or height)
	if limit == None or limit == 0:
		print("Error with the limiting dimension")
		print("Width received:", width)
		print("Higth received:", height)
		return None

	# Gets Zabbix map
	this_map = zapi.map.get(
		sysmapids=sysmapid,
		output="extend",
		selectSelements="extend",
		selectLinks="extend"
	)

	# Gets map's elements
	selements = this_map[0]["selements"]

	x = 0
	y = 0

	print("limit:", limit)
	print("spacement:", spacement)
	print("(x0,y0): ({},{})".format(x0,y0))

	# Creates the new elements
	for host in hosts:

		# Update next position
		# Filling by line
		if width:
			x = (counter % limit) * spacement
			y = (counter // limit) * spacement
			counter += 1

		# Make filling by column
		elif column:
			pass

		new_selement = {
			"elements": [host],
			"elementtype": 0,
			"label": host["name"][7:],
			"iconid_off": iconid,
			"iconid_on": iconid,
			"sysmapid": sysmapid,
			"x": x + x0,
			"y": y + y0,
		}

		selements.append(new_selement)

	zapi.map.update(sysmapid=sysmapid, selements=selements)
