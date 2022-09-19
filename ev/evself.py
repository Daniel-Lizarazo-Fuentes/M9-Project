from settings.constants import *
from settings.variables import *

# With this function, a planning for the operation (i.e. control actions) can be implemented
def evself(ev, prices, co2, profile, lossfree):
	# FIXME: This is a placeholder that needs to be implemented

	# result parameter:
	planning = []

	# ev parameters can be obtained as follows
	# ev.evsoc              # State of Charge of the EV in kWh
	# ev.evminsoc           # Minumum State of Charge of the EV in kWh
	# ev.evcapacity         # Capacity of the EV in kWh
	# ev.evpmin             # Minimum powyr of the EV in W
	# ev.evpmax             # Maximum power of the EV in W

	# Timing variables:
	# ev.evenergy 	        # Energy demand in kWh per driving session
	# ev.evminsoc  	        # Minimum SoC to reach after each session (because of driving)
	# ev.evconnectiontime   # Hours the EV is connected
	# ev.evarrivalhour 	    # Hour of arrival of the EV each day

	# Other input
	# prices, co2, and profile are vectors (lists) with equal length

	# Fallback implementation: Greedy:
	for i in range(0, len(profile)):
		planning.append(ev.evpmax)

	# Finally, the resulting planning for the device must be returned
	# This is also a list, with each value representing the power consumption (average) during an interval in Watts
	# The length of this list must be equal to the input vectors (i.e., prices, co2 and profile)
	return planning