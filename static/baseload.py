from settings.constants import *
from helpers.helpers import *

class Baseload():
	def __init__(self, house):
		self.name = "Baseload"
		self.house = house
		self.number = self.house.housenumber
		self.type = "load"

		self.initialize()
		
		# Planning/control variable
		self.planning = [] # This list contains the control actions required
		
	# Simulation code
	def execute(self, objective, prices, co2, profile, lossfree=True):
		# initialize the device
		self.initialize()

		# pre validation
		try:
			self.verify_input()
		except:
			print("The input parameters for device " + str(self.name) + " of house "+str(self.number) +" are invalid! Aborting!")
			exit()


		# if we have succss, give back the resulting profile
		self.profile = csvToList('data/baseload.csv', self.number, cfg_sim['startInterval'], cfg_sim['startInterval'] + cfg_sim['intervals'])
		return self.profile

	# Function to initialize the results
	def initialize(self):
		# initialize with empty profile
		self.profile = [0] * cfg_sim['intervals']

	# Function to verify the created planning by the optimization code
	# But also to verify user input, is it valid input?
	def verify_input(self):
		csvToList('data/baseload.csv', self.number, cfg_sim['startInterval'], cfg_sim['startInterval'] + cfg_sim['intervals'])
