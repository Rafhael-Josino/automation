'''
This code calculates the avarage network device interface ingoing traffic by week,
separating in two periods as it intends to compare the network consume between them
For example, a network provider wants to check how much its service is being consumed
after aquires a new client.

The code returns the avarage traffic by week as it follows:
- A full journey day: 8-12h and 13h-17h
- A half journey day: 8-12h
- A week: 4 full journey days and 1 half jouney day (friday)
This is for a hipotical scenario

The inventory of the itens and days monitored are in the file monitored_days.py
Each week need to be defined simply by its first day.
There are two arrays od mondays represents each a period.

An interface dictionary has the structure:
	{
		"id": string,
		"name": string
	}
where "id" is its item id in the Zabbix
'''

from sys import argv
from datetime import datetime, timedelta
from pyzabbix.api import ZabbixAPI
import zabbixAccess
from get_item_data import get_item_data
from monitored_days import interfaces, days0, days1


zapi = ZabbixAPI(url=zabbixAccess.url, user=zabbixAccess.user, password=zabbixAccess.password)

def collect_week_day(day, itemid, print_data=False, full_journey=True):
	time_from = day.timestamp()
	time_till = (day + timedelta(hours=3)).timestamp()
	
	values1 = get_item_data(zapi, itemid, time_from, time_till)
		
	if full_journey:
		time_from = (day + timedelta(hours=5)).timestamp()
		time_till = (day + timedelta(hours=8)).timestamp()
	
		values2 = get_item_data(zapi, itemid, time_from, time_till)

	if print_data:
		print("Day", day)
		print("Morning period")
		print(values1)
		if full_journey:
			print("Afternoon period")
			print(values2)
		print("\n")

	if full_journey:
		return (values1["value_avg"] + values2["value_avg"]) / 2
	else:
		return values1["value_avg"]

def collect_week(day, itemid, print_data=False):
	if day.weekday():
		print("Must receive a monday")
		return None

	mon = collect_week_day(day, itemid, print_data)
	thi = collect_week_day(day + timedelta(days=1), itemid, print_data)
	wed = collect_week_day(day + timedelta(days=2), itemid, print_data)
	thu = collect_week_day(day + timedelta(days=3), itemid, print_data)
	fri = collect_week_day(day + timedelta(days=4), itemid, print_data, False)

	band = (mon + thi + wed + thu + fri) / 5

	if band >= 1000000:
		band = band / 1000000
		return "{:.2f} Mbps".format(band)
	else:
		band = band / 1000
		return "{:.2f} Kbps".format(band)


for i in interfaces:
	print(i["name"])

	print("Before migration")
	for d in days0:
		start_day = datetime.strptime(d + " 08:00:00", "%d.%m.%Y %H:%M:%S")
		avg = collect_week(start_day, i["id"], False)
		print("Week", d, avg)
	print("After migration")

	for d in days1:
		start_day = datetime.strptime(d + " 08:00:00", "%d.%m.%Y %H:%M:%S")
		avg = collect_week(start_day, i["id"], False)
		print("Week", d, avg)
