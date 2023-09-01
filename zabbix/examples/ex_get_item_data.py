'''
'''

from datetime import datetime, timedelta
from colorama import init
from termcolor import colored
from pyzabbix.api import ZabbixAPI

import zabbixAccess
from get_item_data import get_item_data
from interfaces_OMs import interfaces, days0, days


zapi = ZabbixAPI(url=zabbixAccess.url, user=zabbixAccess.user, password=zabbixAccess.password)
init()


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
		print("Morning period: 8h-12h")
		print(values1)
		if full_journey:
			print("Afternoon period: 13h-17h")
			print(values2)
		print("\n")

	if values1 == None:
		print(colored("No data was collected in {} morning".format(day), "yellow"))
		if full_journey and values2 != None:
			return values2["value_avg"]
		else:
			print(colored("No data was collected in {}".format(day), "red"))
			return None
			
	if full_journey:
		return (values1["value_avg"] + values2["value_avg"]) / 2
	else:
		return values1["value_avg"]


def collect_week(day, itemid, print_data=False):
	if day.weekday():
		print("Must receive a monday")
		return None

	weekdays = [0,0,0,0,0]
	weekdays[0] = collect_week_day(day, itemid, print_data)
	weekdays[1] = collect_week_day(day + timedelta(days=1), itemid, print_data)
	weekdays[2] = collect_week_day(day + timedelta(days=2), itemid, print_data)
	weekdays[3] = collect_week_day(day + timedelta(days=3), itemid, print_data)
	weekdays[4] = collect_week_day(day + timedelta(days=4), itemid, print_data, False)

	band = 0
	valid_days = 0
	for d in weekdays:
		if d != None:
			valid_days += 1
			band += d	
		
	band = band / valid_days
	#band = (mon + thi + wed + thu + fri) / 5

	if band >= 1000000:
		band = band / 1000000
		return "{:.2f} Mbps".format(band)
	else:
		band = band / 1000
		return "{:.2f} Kbps".format(band)


for t in interfaces:
	print(colored(20 * "-", "green"))
	print(colored(t["name"], "green"))
	print(colored(20 * "-", "green"))

	print(colored("Before migration", "green"))
	for d in days0:
		start_day = datetime.strptime(d + " 08:00:00", "%d.%m.%Y %H:%M:%S")
		avg = collect_week(start_day, t["id"])
		print("Week", d, avg)

	print(colored("After migration", "green"))

	for d in days:
		start_day = datetime.strptime(d + " 08:00:00", "%d.%m.%Y %H:%M:%S")
		avg = collect_week(start_day, t["id"])
		print("Week", d, avg)

	print(colored("\n" + (50 * "#") + "\n", "green"))

