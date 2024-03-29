from settings.constants import *
from settings.variables import *

import math
import copy


# This function simulates the behaviour of the device
def evsim(ev, planning, lossfree=True):
    # result parameter:
    profile = []
    for slot in planning:
        profile.append(0)

    def cutCurrent(soc, change):
        if (change > 0):
            if (soc + (change / 1000) > ev.evcapacity):
                change = (ev.evcapacity - soc) * 1000
            if (change > ev.evpmax):
                change = ev.evpmax
        elif (change < 0):
            change = 0

        return change

    # ev parameters can be obtained as follows
    # ev.evsoc              # State of Charge of the EV in kWh
    # ev.evminsoc           # Minumum State of Charge of the EV in kWh
    # ev.evcapacity         # Capacity of the EV in kWh
    # ev.evpmin             # Minimum power of the EV in W
    # ev.evpmax             # Maximum power of the EV in W

    # Timing variables:
    # ev.evenergy 	        # Energy demand in kWh per driving session
    # ev.evminsoc  	        # Minimum SoC to reach after each session (because of driving)
    # ev.evconnectiontime   # Hours the EV is connected
    # ev.evarrivalhour 	    # Hour of arrival of the EV each day

    # Other input
    # planning, which is the planning created for the device with desired control (power) actions

    # Running the simulation of the device

    # What is already given is to determine if the EV is connected to the charging station (at home) or not (driving)
    intervals_per_day = (3600 / cfg_sim['timebase']) * 24
    intervals_per_hour = (3600 / cfg_sim['timebase'])

    soc = copy.deepcopy(ev.evsoc)

    for i in range(0, len(planning)):

        change = 0

        # Helpers to calculate availability
        arrival_day = math.floor(i / intervals_per_day)
        arrival_interval = arrival_day * intervals_per_day + ev.evarrivalhour * intervals_per_hour
        departure_interval = arrival_interval + ev.evconnectiontime * intervals_per_hour

        if ev.evarrivalhour + ev.evconnectiontime >= 24:
            if departure_interval - (24 * (3600 / cfg_sim['timebase'])) > i and arrival_interval - (
                    24 * (3600 / cfg_sim['timebase'])) > 0:
                departure_interval -= int(24 * (3600 / cfg_sim['timebase']))
                arrival_interval -= int(24 * (3600 / cfg_sim['timebase']))

        # Moment at which the EV arrives
        if i == arrival_interval:

            soc -= ev.evenergy * (3600 / cfg_sim['timebase'])

        # Interval that the EV is connected (available)
        if i >= arrival_interval and i < departure_interval:
            change = cutCurrent(soc, planning[i])

            if (i == departure_interval - 1):
                change = cutCurrent(soc, ev.evpmax)
            profile[i] = change

            soc += change / 1000

        else:
            # Interval that the EV is disconnected (unavailable)
            pass

        if i == departure_interval:

            # Moment at which the EV departs
            pass

    # Finally, the resulting power profile for the devicee must be returned
    # This is also a list, with each value representing the power consumption (average) during an interval in Watts
    # The length of this list must be equal to the input planning list

    return profile
