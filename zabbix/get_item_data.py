'''
Get data from a item by hourly intervals

Each interval posses the data below:
- max value found
- min value found
- avarage values

This function returns the max value, the min value and the avarage value
calculated from all avarages values by hour
'''

from datetime import datetime

def get_item_data(zapi, itemids, time_from, time_till):
	try:
		trend = zapi.trend.get(
			itemids=itemids,
			time_from=time_from,
			time_till=time_till,
			output=[
				"itemid",
				"clock",
				"num",
				"value_min",
				"value_avg",
				"value_max"
			]
		)

		min_array = list(map(lambda t: int(t["value_min"]), trend))
		avg_array = list(map(lambda t: int(t["value_avg"]), trend))
		max_array = list(map(lambda t: int(t["value_max"]), trend))

		'''
		for t in trend:
			print(t, end=" ")
			print("Clock:", datetime.fromtimestamp(int(t["clock"])))
		'''

		return {
			"value_min": min(min_array),
			"value_avg": sum(avg_array)/len(avg_array),
			"value_max": max(max_array),
		}
	
	except Exception as e:
		print("Failed\n{}".format(e.__str__()))
