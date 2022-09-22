from settings.constants import *
from settings.variables import *

import copy


# With this function, a planning for the operation (i.e. control actions) can be implemented
def batteryco2(battery, prices, co2, profile, lossfree):
    # result parameter:
    planning = []
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

        avgCO2 = sum(co2) / len(co2)
        # Fallback implementation: Greedy:
        for i in range(0, len(profile)):
            change = 0
            # User needs power, so discharge battery
            if (profile[i] >= 0):

                change = -profile[i]
            # User has too much power, so charge battery
            else:

                change = -profile[i]

            planning.append(change)

    else:
        # Lossy implementation

        # Fallback implementation: Greedy:
        for i in range(0, len(profile)):
            planning.append(-profile[i])

    # Finally, the resulting planning for the device must be returned
    # This is also a list, with each value representing the power consumption (average) during an interval in Watts
    # The length of this list must be equal to the input vectprs (i.e., prices, co2 and profile)

    return planning
