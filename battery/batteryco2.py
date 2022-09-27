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
                change = -(soc - battery.batminsoc) * 1000
            if (change < battery.batpmin):
                change = battery.batpmin

        return change

    def findIndexNextCharge(i, profile):
        while (i < len(profile) - 1 and profile[i] <= 0):
            i += 1
        return i;

    # result parameter:
    planning = []
    tempProfile = []
    for slot in profile:
        planning.append(0)
        tempProfile.append(-slot)
    socValues = []

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
        # Fill aray based on CO2
        for i in range(0, len(tempProfile)):
            change = 0

            try:
                indexNextRequestedBatteryCharge = findIndexNextCharge(i, tempProfile);

                # Requested discharge
                if (tempProfile[i] < 0):

                    # Check if the sum of changes requested until the next battery charge are smaller than soc.
                    if (soc + (sum(tempProfile[i:indexNextRequestedBatteryCharge]) / 1000) < battery.batminsoc):

                        # If Co2 below average in the interval
                        if (co2[i] < (sum(co2[i:indexNextRequestedBatteryCharge]) / len(
                                co2[i:indexNextRequestedBatteryCharge]))):
                            change = -((soc * 1000) - sum(profile[i:indexNextRequestedBatteryCharge]))

                        # If Co2 is above average
                        else:
                            change = tempProfile[i]

                    else:
                        change = tempProfile[i]

                # Requested charge
                elif (tempProfile[i] > 0):
                    change = tempProfile[i]
                # No usage
                else:
                    pass



            except IndexError:
                change = tempProfile[i]

            # haircuts the change
            change = cutCurrent(soc, change)
            planning[i] = change
            soc += change / 1000
            socValues.append(soc)

    else:
        # Lossy implementation

        # Fallback implementation: Greedy:
        for i in range(0, len(profile)):
            planning.append(-profile[i])

    # Finally, the resulting planning for the device must be returned
    # This is also a list, with each value representing the power consumption (average) during an interval in Watts
    # The length of this list must be equal to the input vectprs (i.e., prices, co2 and profile)
    return planning
