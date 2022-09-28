from settings.constants import *
from settings.variables import *

import math
import copy


# With this function, a planning for the operation (i.e. control actions) can be implemented
def evco2(ev, prices, co2, profile, lossfree):
    # result parameter:
    planning = []
    tempProfile = []
    for slot in profile:
        planning.append(0)
        if (-slot < 0):
            tempProfile.append(0)
        else:
            tempProfile.append(-slot)

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
    # ev.evpmin             # Minimum powyr of the EV in W
    # ev.evpmax             # Maximum power of the EV in W

    # Timing variables:
    # ev.evenergy 	        # Energy demand in kWh per driving session
    # ev.evminsoc  	        # Minimum SoC to reach after each session (because of driving)
    # ev.evconnectiontime   # Hours the EV is connected
    # ev.evarrivalhour 	    # Hour of arrival of the EV each day

    intervals_per_day = (3600 / cfg_sim['timebase']) * 24
    intervals_per_hour = (3600 / cfg_sim['timebase'])

    soc = copy.deepcopy(ev.evsoc)

    # Other input
    # prices, co2, and profile are vectors (lists) with equal length
    for i in range(0, len(tempProfile)):
        change = 0
        arrival_day = math.floor(i / intervals_per_day)
        arrival_interval = arrival_day * intervals_per_day + ev.evarrivalhour * intervals_per_hour
        departure_interval = arrival_interval + ev.evconnectiontime * intervals_per_hour

        # Moment at which the EV arrives
        if i == arrival_interval:
            soc -= ev.evenergy

        # Interval that the EV is connected (available)
        if i >= arrival_interval and i < departure_interval:

            iEnd = int(departure_interval - 1)
            # Check if the sum of charges in the interval + soc is greater than min soc
            if (soc + sum(tempProfile[i:iEnd]) >= ev.evcapacity):
                change = tempProfile[i]

            # Need to charge additionaly to renewable
            else:
                requiredAdditionalCharge = ev.evcapacity - soc - (sum(tempProfile[i:iEnd]) / 1000)

                try:
                    # If Co2 below average in the interval
                    if (co2[i] < (sum(co2[i:iEnd]) / len(
                            co2[i:iEnd]))):
                        change = requiredAdditionalCharge * 1000
                except ZeroDivisionError:
                    change = requiredAdditionalCharge * 1000


                # If Co2 is above average
                else:
                    pass

            change = cutCurrent(soc, change)
            if (i == iEnd):
                change = cutCurrent(soc, ev.evpmax)
            planning[i] = change

            soc += change / 1000


    else:
        # Interval that the EV is disconnected (unavailable)
        pass

    if i == departure_interval:
        # Moment at which the EV departs
        pass

    # Finally, the resulting planning for the device must be returned
    # This is also a list, with each value representing the power consumption (average) during an interval in Watts
    # The length of this list must be equal to the input vectors (i.e., prices, co2 and profile)

    return planning
