from settings.constants import *
from settings.variables import *

from helpers.helpers import *

class PV():
	def __init__(self, house):
		# FIXME variables
		self.name = "PV"
		self.house = house
		self.number = self.house.housenumber
		self.column = 0
		self.type = "generator"

		# FIXME BASED ON INPUT
		# Defautl parameters
		self.filename = 'data/pv.csv'
		self.pvpanels = 1

		self.pvazimuth = 180
		self.pvtilt = 35

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

		returnprofile = csvToList(self.filename, self.column, cfg_sim['startInterval'], cfg_sim['startInterval'] + cfg_sim['intervals'])
		for i in range(0, len(returnprofile)):
			returnprofile[i] *= self.pvpanels

		self.profile = returnprofile
		return self.profile


	# Function to initialize the results
	def initialize(self):
		# initialize with empty profile
		self.profile = [0] * cfg_sim['intervals']
		self.planning = [0] * cfg_sim['intervals']

		# PVsettings
		try:
			self.pvpanels = cfg_houses[self.number]["pvpanels"]
			self.pvazimuth = cfg_houses[self.number]["pvazimuth"]
			self.pvtilt = cfg_houses[self.number]["pvtilt"]

			# Determine the column to read based on the config provided
			azimuth = ["east", "southeast", "south", "southwest", "west"]
			tilt = [10, 15, 20, 25, 30, 35, 40, 45, 50]
			self.column = azimuth.index(self.pvazimuth) * 9 + tilt.index(self.pvtilt)

		except:
			print("Input for PV panel " + str(self.number) + " is invalid!")
			exit()


	# Function to verify the created planning by the optimization code
	# But also to verify user input, is it valid input?
	def verify_input(self):
		csvToList(self.filename, self.column, cfg_sim['startInterval'], cfg_sim['startInterval'] + cfg_sim['intervals'])
		assert(self.pvpanels >= 0)

