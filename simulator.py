#!/usr/bin/python3

from groupinfo import *
from settings.constants import *
from settings.variables import *
from helpers.helpers import *

# house simulaiton imports
from static.house import House

import os



# Initial configuration check
try:
	assert(group_number>0)
	if group_members >= 1:
		assert(group_member_1_name != '')
		assert(group_member_1_number != 's' and len(group_member_1_number) == 8)
		assert(group_member_1_study != '')
	if group_members >= 2:
		assert(group_member_2_name != '')
		assert(group_member_2_number != 's' and len(group_member_2_number) == 8)
		assert(group_member_2_study != '')
	if group_members >= 3:
		assert(group_member_3_name != '')
		assert(group_member_3_number != 's' and len(group_member_3_number) == 8)
		assert(group_member_3_study != '')
except:
	print("Please first fill your student group information!")
	exit()


# Loading config
# Select optimization objectives?

# Instantiate houses
houses = []
for housenumber in cfg_houses.keys():
	if housenumber >= 80:
		print("Only house indexes up to 79 are allowed in the house config.")
		exit()

	assert(housenumber < 80 and housenumber >= 0)
	# Create and initialize a house
	house = House(housenumber)

	if not house.verify_input():
		print("Configuration provided for house number "+str(housenumber)+" is invalid. Check your variables file. Exiting the simulation")
		exit()

	houses.append(house)


# Input data
profile = [0] * cfg_sim['intervals']
prices  = csvToList('data/prices.csv', 0, cfg_sim['startInterval'], cfg_sim['startInterval'] + cfg_sim['intervals'])
co2     = csvToList('data/co2.csv', 0, cfg_sim['startInterval'], cfg_sim['startInterval'] + cfg_sim['intervals'])

assert(len(profile) == len(prices) == len(co2))

lossfree = True
errorflag = False

# Remove the old results
file = cfg_sim['outputfile']
if os.path.exists(file):
	os.remove(file)

# Write student group stats:
write_result(cfg_sim['outputfile'], "student_group_number", [group_number])
if group_members >= 1:
	write_result(cfg_sim['outputfile'], "student_1", [group_member_1_name, group_member_1_number, group_member_1_study])
if group_members >= 2:
	write_result(cfg_sim['outputfile'], "student_2", [group_member_2_name, group_member_2_number, group_member_2_study])
if group_members >= 3:
	write_result(cfg_sim['outputfile'], "student_3", [group_member_3_name, group_member_3_number, group_member_3_study])



# Remove the old results
overviewfile = cfg_sim['overviewfile']
if os.path.exists(overviewfile):
	os.remove(overviewfile)

# Print scores:
print("---------------------------------------------------------------------------------------------------------------------------------")
print("|\t\t| cost \t| co2 \t| 1-norm\t| 2-norm\t| inf-norm\t| dmnd\t| selfs\t| net\t| SUI\t| LCF\t| SCF\t|")
print("|\t\t| €\t| g\t| W\t\t| W\t\t| Wm\t\t| kWh\t| kWh\t| kWh\t| -\t| -\t| -\t|")
print("---------------------------------------------------------------------------------------------------------------------------------")

write_result(cfg_sim['overviewfile'], ",", ["cost, co2 emissions, 1-norm, 2-norm, inf-norm, demand, selfconsumption, net metering, SUI, LCF, SCF"])
write_result(cfg_sim['overviewfile'], ",", ["EUR, grammes of CO2, Watt, Watt, Watt, kWh, kWh, kWh, ratio, ratio, ratio"])
write_result(cfg_sim['overviewfile'], ",", ["energy price without taxes, total emissions, self consumption metric, flatness, biggest peak, total consumed energy, genertion directly consumed, net metered energy, sustainability index factor, load coverage factor (how much demand was overall matched by local generation), storage coverage factor (how much of demand was supplied by storage)"])

# Run all optimization objectives, at least try to
for lossfree in [True, False]:
	print(" ")

	# Selection of objectives
	objectives_selection = objectives
	if not lossfree:
		objectives_selection = objectives_losses

	for objective in objectives_selection:
		lossstr = "_lossfree"
		if lossfree:
			print("Loss free simulation - Objective: ", objective)
		else:
			print("Lossy simulation - Objective: ", objective)
			lossstr = "_lossy"

		# Stats printing
		o = objective.replace("imize", '')
		if objective == "optimize_profile_flatness":
			o = "opt_flatness"
		elif objective == "optimize_self_consumption":
			o = "opt_self"

		print("---------------------------------------------------------------------------------------------------------------------------------")
		print("| "+o+"\t| cost \t| co2 \t| 1-norm\t| 2-norm\t| inf-norm\t| dmnd\t| selfs\t| net\t| SUI\t| LCF\t| SCF\t|")
		print("---------------------------------------------------------------------------------------------------------------------------------")

		# Overall profile bookkeeping of the neighbourhood of houses:
		demand = [0] * cfg_sim['intervals']
		supply = [0] * cfg_sim['intervals']
		storage = [0] * cfg_sim['intervals']
		aggregate = [0] * cfg_sim['intervals']

		# Simulate houses with objectives
		for house in houses:
			# Simulate each house
			errorflag = house.execute(objective, prices, co2, profile, lossfree)

			if not errorflag:
				demand = [sum(x) for x in zip(demand, house.demand)]
				supply = [sum(x) for x in zip(supply, house.supply)]
				storage = [sum(x) for x in zip(storage, house.storage)]
				aggregate = [sum(x) for x in zip(aggregate, house.aggregate)]

				house.store_result(file, objective+lossstr)

			else:
				print("Simulation of house " + str(house.housenumber) + " failed! Aborting simulation")
				# Remove the results
				file = cfg_sim['outputfile']
				if os.path.exists(file):
					os.remove(file)
				exit()

		scores = obtain_scores("Neighbourhood "+objective+lossstr, aggregate, demand, supply, storage, prices, co2, profile)
		# make print function
		s = "| Neighbourhood\t| "
		for score in scores:
			s += score + "\t| "
		print(s)
		print("---------------------------------------------------------------------------------------------------------------------------------")
		print(" ")

		# And lets store these results in a useful csv too
		write_result(cfg_sim['overviewfile'], objective+lossstr+",Neighbourhood", scores)




if not errorflag:
	print("Simulation successful")

input("Press Enter to exit.")