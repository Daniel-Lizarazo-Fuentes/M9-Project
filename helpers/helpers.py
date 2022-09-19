from settings.constants import *

import math

def csvToList(file, column, start, end, delimiter=';'):
	result = []
	
	f = open(file, 'r')
	ln = 0
	for line in f:
		if ln >= start and ln < end:
			s = line.strip()
			s = line.split(delimiter)
			try:
				s = float(s[column])
			except:
				s = 0.0
			result.append(s)
		if ln >= end:
			break
		ln +=1
		
	f.close()
	
	return result
	
def write_result(file, name, data):
	assert(isinstance(data, list))
	f = open(file, 'a+')
	s = name+", "+str(data)+"\n"
	s = s.replace("'", '')
	s = s.replace('[', '')
	s = s.replace(']', '')
	f.write(s)
	f.close()




def obtain_scores(simulation_name, aggregated, demand, supply, storage, prices, co2, profile):
	assert(len(profile) == len(aggregated) == len(demand) == len(supply) == len(prices) == len(co2))

	result = []

	name = simulation_name
	# Metrics based on the objective functions

	# Cost reduction
	costs = 0
	for i in range(0, len(prices)):
		costs += ( (aggregated[i] * (0.001*cfg_sim['timebase']/3600)) * prices[i])
	# print(name+" total costs: "+str(costs))
	result.append(str("%.2f" % costs))


	# CO2 emissions
	emissions = 0
	for i in range(0, len(co2)):
		imported = max(0, (aggregated[i] * (0.001*cfg_sim['timebase']/3600)))
		emissions += imported * co2[i]
	# print(name+" total emissions: "+str(emissions)) # grams
	result.append(str("%.0f" % emissions))

	# difference vector:
	diff_vector = []
	for i in range(0, len(aggregated)):
		diff_vector.append(abs(aggregated[i] - profile[1]))

	# 1-norm
	norm_one = 0
	for value in diff_vector:
		norm_one = norm_one+math.sqrt(value)
	# print(name + " 1-norm score: " + str(norm_one))
	result.append(str("%.2E" % norm_one))

	# 2 norm
	norm_two = 0
	for value in diff_vector:
		norm_two = norm_two + pow(value, 2)
		norm_two = math.sqrt(norm_two)
	# print(name + " 2-norm score: " + str(norm_two))
	result.append(str("%.2E" % norm_two))

	# inifinity norm
	norm_max = max(diff_vector)
	# print(name + " infinity-norm score: " + str(norm_max))
	result.append(str("%.2E" % norm_max))

	# total demand
	total_demand = sum(demand) * (0.001 * cfg_sim['timebase'] / 3600)
	result.append(str("%.0f" % total_demand))

	# self-consumption
	selfconsumption = 0.0
	for i in range(0, len(demand)):
		selfconsumption += min(abs(supply[i]), demand[i])
	selfconsumption = selfconsumption * (0.001 * cfg_sim['timebase'] / 3600)
	# print(name + " direct selfconsumption: " + str(selfconsumption) + ' kWh')
	result.append(str("%.0f" % selfconsumption))

	# net metering
	total_demand = sum(demand)
	total_supply = abs(sum(supply))
	net_metering = total_supply
	if total_demand < total_supply:
		net_metering = total_demand
	net_metering = net_metering * (0.001*cfg_sim['timebase']/3600)
	# print(name + " net metered consumption: " + str(net_metering) + ' kWh')
	result.append(str("%.0f" % net_metering))

	# SUI: https://www.nrel.gov/docs/fy20osti/77415.pdf
	sust_use_index = selfconsumption / (sum(demand) * (0.001 * cfg_sim['timebase'] / 3600) )
	# print(name + " sustainable energy use index: " + str(sust_use_index) + ' (directly used energy as fraction of total demand)')
	result.append(str("%.2f" % sust_use_index))


	# load coverage factor
	lcf = (abs(sum(supply)) / (sum(demand)))
	# print(name + " load coverage factor: " + str(lcf) + '% (energy generated of total demand)')
	result.append(str("%.2f" % lcf))

	# Energy through battery
	storage_energy = 0
	for value in storage:
		if value < 0:
			storage_energy += abs(value)
	storage_energy = storage_energy * (0.001*cfg_sim['timebase']/3600)
	# print(name + " energy supplied by the battery: " + str(storage_energy) + ' kWh')

	# Storage coverage factor
	storage_delivered = 0
	for value in storage:
		if value < 0:
			storage_delivered += abs(value)
	lcfs = (storage_delivered / (sum(demand)))
	# print(name + " load coverage factor by storage: " + str(lcfs) + '% (energy supplied by storage as factor of total demand)')
	result.append(str("%.2f" % lcfs))

	return result

	# cost, co2, n1, n2, ni, d, sc, nm, sui, lcf, scf