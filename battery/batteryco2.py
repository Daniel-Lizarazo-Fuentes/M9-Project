from settings.constants import *
from settings.variables import *

import copy

# With this function, a planning for the operation (i.e. control actions) can be implemented
def batteryco2(battery, prices, co2, profile, lossfree):
	# result parameter:
	planning = []
	for slot in profile:
		planning.append(0)
	# Battery parameters can be obtained as follows
	# battery.batsoc        # State of Charge in kWh
	# battery.batminsoc     # Minimum State of Charge
	# battery.batcapacity   # Capacity of the battery in kWh
	# battery.batpmin       # Maximum power in W
	# battery.batpmax       # Minimum power in W

	# Other input
	# prices, co2, and profile are vectors (lists) with equal length

	if lossfree:
		# Loss free implementation
		soc = copy.deepcopy(battery.batsoc)
		for i in range(0, len(profile)):
			change = 0

			if (profile[i] < 0):
				if (soc + (profile[i] / 1000) >= battery.batminsoc):
					change = profile[i]

				else:
					change = -(soc - battery.batminsoc) * 1000

			elif (profile[i] > 0):
				if (co2[i] < (sum(co2) / len(co2))):
					# Check if battery is at full capacity
					if (soc + (profile[i] / 1000) < battery.batcapacity):
						change = profile[i]
					else:
						change = (battery.batcapacity - soc) * 1000

			if (change < 0 and change < -battery.batpmax):
				change = -battery.batpmax
			elif (change > 0 and change > battery.batpmax):
				change = battery.batpmax
			planning[i] = change
			soc += change / 1000


	else:
		# Lossy implementation

		# FIXME: Placeholder implementation
		# Fallback implementation: Greedy:
		for i in range(0, len(profile)):
			planning.append(-profile[i])

	# Finally, the resulting planning for the device must be returned
	# This is also a list, with each value representing the power consumption (average) during an interval in Watts
	# The length of this list must be equal to the input vectprs (i.e., prices, co2 and profile)
	return planning