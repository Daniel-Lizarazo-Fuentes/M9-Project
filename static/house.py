from settings.constants import *
from settings.variables import *
from helpers.helpers import *



from static.baseload import Baseload
from static.pv import PV
from static.windturbine import Windturbine
from static.ev import EV
from static.battery import Battery

class House():
	def __init__(self, housenumber):
		self.housenumber = housenumber
		self.name = "House-"+str(self.housenumber)
		
		# Add the devices of this house
		self.devices = []
		self.devices.append(Baseload(self))
		self.devices.append(PV(self))
		self.devices.append(Windturbine(self))
		self.devices.append(EV(self))
		self.devices.append(Battery(self))

		# Storage for statistics
		self.demand = []
		self.supply = []
		self.storage = []

		
	# Optimize and simulate the devices in the household
	def initialize(self):
		# initialize with empty profile
		self.aggregate = [0] * cfg_sim['intervals']
		self.planning = [0] * cfg_sim['intervals']

		self.demand = [0] * cfg_sim['intervals']
		self.supply = [0] * cfg_sim['intervals']
		self.storage = [0] * cfg_sim['intervals']
		
	
	def execute(self, objective="greedy", prices=[], co2=[], profile=[], lossfree=True):
		errorflag = False

		self.initialize()

		# Simulate all devices
		for device in self.devices:
			# Simulate the device
			p = device.execute(objective, prices, co2, self.aggregate, lossfree)
			
			assert(len(p) == len(profile))

			self.aggregate = [sum(x) for x in zip(p, self.aggregate)]

			# Unsure if we need global params here
			if device.type == "load":
				self.demand = [sum(x) for x in zip(p, self.demand)]
			elif device.type == "generator":
				self.supply = [sum(x) for x in zip(p, self.supply)]
			elif device.type == "storage":
				self.storage = [sum(x) for x in zip(p, self.storage)]


		# Verify validity of the result:
		# Enfore battery size restrictions, which is conveniently the last device
		# first obtain average daily demand
		avg_demand = (sum(self.demand)*0.001*(cfg_sim['timebase'] / 3600.0)) / ((cfg_sim['intervals'] * cfg_sim['timebase']) / (24*3600))
		if self.devices[-1].batcapacity > avg_demand * cfg_sim['bat_maxcapacity']:
			print("The Battery capacity of house "+str(self.housenumber)+" is too large. Its capacity is allowed to be a maximum of "+str(cfg_sim['bat_maxcapacity'])+" times the average daily demand. The average demand is "+str(avg_demand)+" kWh, hence the allowed storage capacity is "+str(avg_demand*cfg_sim['bat_maxcapacity'])+" kWh")
			exit()

		lcf = abs(sum(self.supply)/sum(self.demand))
		if lcf > cfg_sim['res_coverage']:
			print("The total generation of house" + str(self.housenumber) + " is too large. The allowed maximum load coverage factor (i.e. supply/demand-ratio) is" + str( cfg_sim['res_coverage']) + ". Your total current generation is "+str(sum(self.supply)*-0.001*(cfg_sim['timebase'] / 3600.0))+" kWh and total demand is "+str(sum(self.demand)*0.001*(cfg_sim['timebase'] / 3600.0))+" kWh")
			exit()

		scores = obtain_scores(self.name+" "+objective, self.aggregate, self.demand, self.supply, self.storage, prices, co2, profile)

		# make print function
		s = "| "+self.name+"\t| "
		for score in scores:
			s += score + "\t| "
		print(s)

		# Write the results to a CSV too:
		write_result(cfg_sim['overviewfile'], objective+","+self.name, scores)

		return errorflag



	def verify_input(self):
		return self.housenumber in cfg_houses


	def store_result(self, file, name):
		name += '_house_'+str(self.housenumber)

		# Write the houseprofile
		write_result(file, name, self.aggregate)

		# Write device profiles
		for device in self.devices:
			write_result(file, name+"_device_"+str(device.name), device.profile)
