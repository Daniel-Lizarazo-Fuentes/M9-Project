from settings.constants import *
from settings.variables import *

from helpers.helpers import *

import math

class Windturbine():
	def __init__(self, house):
		# FIXME variables
		self.name = "Windturbine"
		self.house = house
		self.number = self.house.housenumber
		self.type = "generator"

		# FIXME BASED ON INPUT
		# Default parameters
		self.filename = 'data/windspeed.csv'
		self.winddiameter = 1

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

		returnprofile = []
		windspeed = csvToList(self.filename, 0, cfg_sim['startInterval'], cfg_sim['startInterval'] + cfg_sim['intervals'])
		for i in range(0, len(windspeed)):
			# Determine production, bear in mind that production is negative
			# https://www.e-education.psu.edu/emsc297/node/649#:~:text=The%20formula%20is%20capacity%20factor,yr%20(or%20832.2%20MWh).
			production = -1 * 0.5 * 1.225 * math.pi * pow(self.winddiameter * 0.5, 2) * pow(windspeed[i], 3)
			returnprofile.append(production)

		self.profile = returnprofile
		return self.profile


	# Function to initialize the results
	def initialize(self):
		# initialize with empty profile
		self.profile = [0] * cfg_sim['intervals']
		self.planning = [0] * cfg_sim['intervals']

		# PVsettings
		try:
			self.winddiameter = cfg_houses[self.number]["winddiameter"]

		except:
			print("Input for Windturbine " + str(self.number) + " is invalid!")
			exit()

		if self.winddiameter > cfg_sim['wind_maxdiameter']:
			print("The diameter for Windturbine " + str(self.number) + " may not exceed 5m!")
			exit()


	# Function to verify the created planning by the optimization code
	# But also to verify user input, is it valid input?
	def verify_input(self):
		csvToList(self.filename, 0, cfg_sim['startInterval'], cfg_sim['startInterval'] + cfg_sim['intervals'])
		assert(self.winddiameter >= 0)
