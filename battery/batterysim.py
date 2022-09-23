from settings.constants import *
from settings.variables import *

import copy


# This function simulates the behaviour of the device
def batterysim(battery, planning, lossfree=True):
    def cutCurrent(soc, change):
        if (change > 0):
            if (soc + (change / 1000) >= battery.batcapacity):
                change = (battery.batcapacity - soc) * 1000
            if (change > battery.batpmax):
                change = battery.batpmax
        elif (change < 0):
            if (soc + (change / 1000) <= battery.batminsoc):
                change = (soc-battery.batminsoc) * 1000
            if (change < battery.batpmin):
                change = battery.batpmin

        return change

    # result parameter to be filled:
    profile = []
    for slot in planning:
        profile.append(0)
    # Battery parameters can be obtained as follows
    # battery.batsoc        # State of Charge in kWh
    # battery.batminsoc     # Minimum State of Charge
    # battery.batcapacity   # Capacity of the battery in kWh
    # battery.batpmin       # Maximum power in W
    # battery.batpmax       # Minimum power in W

    # Other input
    # planning, which is the planning created for the device with desired control (power) actions

    # Running the simulation of the device

    # Lossfree simulation:
    if lossfree:
        soc = copy.deepcopy(battery.batsoc)
        for i in range(0, len(planning)):
            change = 0
            change = cutCurrent(soc, planning[i])
            profile[i] = change
            soc += change / 1000

    # Here you will need to implement yoor simulation code
    # Create the resulting by filling the profile list
    # This can be done by e.g. profile.append(value)

    # Lossy simulation:
    else:
        pass
    # Here you will need to implement yoor simulation code
    # Create the resulting by filling the profile list
    # This can be done by e.g. profile.append(value)

    # Finally, the resulting power profile for the devicee must be returned
    # This is also a list, with each value representing the power consumption (average) during an interval in Watts
    # The length of this list must be equal to the input planning list

    return profile
