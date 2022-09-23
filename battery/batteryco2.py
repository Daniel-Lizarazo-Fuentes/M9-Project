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
                change = (soc - battery.batminsoc) * 1000
            if (change < battery.batpmin):
                change = battery.batpmin

        return change

    # result parameter:
    planning = []
    for slot in profile:
        planning.append(0)
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
        for i in range(0, len(profile)):
            change = 0

            # c02 of next interval is higher than current:
            try:
                # if (co2[i] < co2[i + 1]):
                #     # If sum of next 4 (incl current) usage values + soc are smaller than battery capacity: fill battery now
                #     if (
                #             ((-sum(profile[i:i + 3])) / 1000) + soc < battery.batcapacity
                #     ):
                #         change = battery.batpmax
                #     else:
                #         change = -profile[i]
                # elif (co2[i] >= co2[i + 1]):
                #     change = -profile[i]
                # else:
                #     change = -profile[i]


                # If Co2 below average
                if(co2[i]<(sum(co2)/len(co2))):
                    if( -profile[i]>0):
                        change = -profile[i]
                    if (
                            ((-sum(profile[i:i+5]) / 1000) + soc) < battery.batcapacity
                    ):
                        change = battery.batpmax

                # If Co2 is abvoe average
                else:
                    if (-profile[i] < 0):
                        change = -profile[i]

            except IndexError:
                change = -profile[i]

            # haircuts the change
            change = cutCurrent(soc, change)
            planning[i] = change
            soc += change / 1000

        # Adjust array based on usage
        # soc = copy.deepcopy(battery.batsoc)
        # for i in range(0, len(profile)):
        #     change = planning[i]
        #
        #     # User discharges and battery discharges
        #     if (planning[i] < 0 and profile[i] < 0):
        #         pass
        #     # User discharges and battery charges
        #     elif (planning[i] > 0 and profile[i] < 0):
        #         pass
        #     # User charges and battery charges
        #     elif (planning[i] > 0 and profile[i] > 0):
        #         pass
        #     # User charges and battery discharges
        #     elif (planning[i] < 0 and profile[i] > 0):
        #         pass
        #
        #     # haircuts the change
        #     change = cutCurrent(soc, change)
        #     planning[i] = change
        #
        #     soc += change / 1000
        #     socValues.append(soc)
        #
        #     # print('\n')
        #     # print(planning[i])
        #     # print(soc)


    else:
        # Lossy implementation

        # Fallback implementation: Greedy:
        for i in range(0, len(profile)):
            planning.append(-profile[i])

    # Finally, the resulting planning for the device must be returned
    # This is also a list, with each value representing the power consumption (average) during an interval in Watts
    # The length of this list must be equal to the input vectprs (i.e., prices, co2 and profile)

    # print('\n')
    # print(co2)
    # print(profile)
    # print(planning)
    # print(socValues)
    # print('\n')

    return planning
