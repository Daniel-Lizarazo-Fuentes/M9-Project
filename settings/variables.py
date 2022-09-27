from groupinfo import *

# Variable settings, these may be modified

# Configuration of the objectives to be simulated by the simulator
# Select optimizations automatically based on the groupinfo.py information provided or not:
automatic = True

# Automatic setup of objectives:
if automatic:
	objectives = []
	objectives_losses = []

	if optimize_greedy:
		objectives.append("optimize_greedy")
	if optimize_prices:
		objectives.append("optimize_prices")
	if optimize_co2:
		objectives.append("optimize_co2")
	if optimize_self:
		objectives.append("optimize_self_consumption")
	if optimize_flat:
		objectives.append("optimize_profile_flatness")

	# Lossy optimization
	if optimize_greedy_loss:
		objectives_losses.append("optimize_greedy")
	if optimize_prices_loss:
		objectives_losses.append("optimize_prices")
	if optimize_co2_loss:
		objectives_losses.append("optimize_co2")

# Manual config of optimizations to be performed
else:
	# Objectives to be simulated without losses
	objectives = ["optimize_greedy"]
	# All options:
	# objectives = ["optimize_greedy", "optimize_prices", "optimize_co2", "optimize_self_consumption", "optimize_profile_flatness"]

	# Select which simulations to perform with losses enabled
	objectives_losses = []
	# objectives_losses =["optimize_greedy", "optimize_prices", "optimize_co2"]



cfg_houses = {
	# First house:	# NOTE THE OFF-BY-ONE COUNTING STARTING AT 0!
	0: {
		# PV configuration
		"pvpanels":  5,  # Number of panels, integer
		"pvazimuth": "south",  # Available options: east, southeast, south, southwest, west
		"pvtilt":  30,  # Available options: 10, 15, 20, 25, 30, 35, 40, 45, 50

		# Wind turbine configuration
		"winddiameter": 3,  # Diameter in metres

		# Battery configuration
		"batminsoc":    0,  # Minimum state of charge in kWh
		"batcapacity":  4,  # Capacity in kWh
		"batsoc":       0,  # Initial State of Charge at start of simulation in kWh
		"batpmin":      -3000,  # Minumum power (discharge is negative) in W
		"batpmax":      3000,  # Maximum power in W
	},

	# Second house:	# NOTE THE OFF-BY-ONE COUNTING!
	1: {
		# PV configuration
		"pvpanels":  1,  # Number of panels, integer
		"pvazimuth": "south",  # Available options: east, southeast, south, southwest, west
		"pvtilt":  30,  # Available options: 10, 15, 20, 25, 30, 35, 40, 45, 50

		# Wind turbine configuration
		"winddiameter": 1,  # Diameter in metres

		# Battery configuration
		"batminsoc":	0,  # Minimum state of charge in kWh
		"batcapacity":  4,  # Capacity in kWh
		"batsoc":       0,  # Initial State of Charge at start of simulation in kWh
		"batpmin":      -3000,  # Minumum power (discharge is negative) in W
		"batpmax":      3000,  # Maximum power in W
	},

	# Copy the configuration for how many houses you have
}