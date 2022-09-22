from settings.constants import *
from settings.variables import *

import copy


# With this function, a planning for the operation (i.e. control actions) can be implemented
def batteryco2(battery, prices, co2, profile, lossfree):
    def cutCurrent(soc, change):
        if (change > 0):
            if (soc + (change / 1000) > battery.batcapacity):
                change = (battery.batcapacity - soc) * 1000
            if (change > battery.batpmax):
                change = battery.batpmax
        elif (change < 0):
            if (soc + (change / 1000) < battery.batminsoc):
                change = (soc-battery.batminsoc) * 1000
            if (change < battery.batpmin):
                change = battery.batpmin

        return change

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
    soc = copy.deepcopy(battery.batsoc)
    if lossfree:
        # Loss free implementation
        for i in range(0, len(profile)):
            change = 0

            # if battery is not full and c02 of next interval is higher than current:
            if(soc < battery.batcapacity and i < len(co2) - 1 and co2[i] < co2[i + 1]):
                # Python <3.10 doesn't have a switch so here a large if else series
                if():
                    pass


            cutCurrent(soc, change)

            soc += change / 1000
            planning[i] = change

            # print('\n')
            # print(planning[i])
            # print(soc)

    else:
        # Lossy implementation

        # Fallback implementation: Greedy:
        for i in range(0, len(profile)):
            planning.append(-profile[i])

    # Finally, the resulting planning for the device must be returned
    # This is also a list, with each value representing the power consumption (average) during an interval in Watts
    # The length of this list must be equal to the input vectprs (i.e., prices, co2 and profile)

    print('\n')
    print(co2[0:45])
    print(profile[0:45])
    print(planning[0:45])
    print('\n')

    return planning
