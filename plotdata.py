#!/usr/bin/python3

# Tool to plot the output files. Feel free to modify this script to your own liking for analysis

from groupinfo import *
from settings.constants import *
from settings.variables import *
from helpers.helpers import *
import matplotlib.pyplot as plt

# Plot settings
# default reads from the configuration file
plot_objectives = objectives
# Manual selection by:
# plot_objectives = ["optimize_greedy", "optimize_prices", "optimize_co2", "optimize_self_consumption", "optimize_profile_flatness"]

# Objectives with losses
plot_objectives_losses = objectives_losses
# Manual selection by:
# plot_objectives_losses = ["optimize_greedy", "optimize_prices", "optimize_co2"]

# Select the houses to plot
plot_houses = cfg_houses.keys()
# Alternatively, you can fill a list with houses to plot
# plot_houses = [0, 1, 2] # Note that we start counting at 0

# Which device profiles to plot:
plot_devices = ['Aggregate', 'Baseload', 'PV', 'Windturbine', 'Electricvehicle', 'Battery']
# plot_devices = ['Aggregate', 'Baseload', 'PV', 'Windturbine', 'Electricvehicle', 'Battery']

# Which intervals to plot (maximum range is [0, 672], which is off-by one, meaning dat it plots intervals 1-672, or list indexes 0 up to and including 671)
plot_startinterval = 0
plot_endinterval = 672


# Plotting style:
plt.style.use('_mpl-gallery')


# Load the file
try:
    f = open(cfg_sim['outputfile'], 'r')
except:
    print("No suitable results.csv file found!")
    exit()

# Load the contents in a convenient way
contents = {}
for line in f:
    try:
        line = line.strip()

        # in case Matlab generated results are plotted using python, lets get rid of the last ',':
        if line[-1] == ',':
            line = line[0:-1]

        line = line.split(",")
        l = []
        for v in range(1, len(line)):
            l.append(float(line[v]))

        contents[line[0]] = l
    except:
        pass

f. close()

print("This will attempt to create all plots, press Ctrl+C to abort")


assert(plot_startinterval >= 0)
assert(plot_endinterval <= 672)
assert(plot_startinterval <= plot_endinterval)
x = list(range(plot_startinterval, plot_endinterval))

for house in plot_houses:
    for lossfree in [True, False]:
        obj = objectives
        strl = "lossfree"
        if not lossfree:
            obj = objectives_losses
            strl = "lossy"

        for objective in obj:
            plt.figure(figsize=(20, 8))

            for device in plot_devices:
                # compose the search string
                s = objective+'_'+strl+"_house_"+str(house)
                if device != "Aggregate":
                    s+= '_device_'+device

                # now find this in the data
                if s not in contents:
                    print("Error, data does not exist ", s)
                y = contents[s][plot_startinterval:plot_endinterval]

                # creat the plot
                plt.step(x, y, where='post', label=device)


            print("Plotting house "+str(house)+" with objective "+objective+"_"+strl)
            plt.title('House '+str(house)+" with objective "+objective+"_"+strl)
            plt.grid(axis='x', color='0.95')
            plt.grid(axis='y', color='0.95')
            plt.legend(title='Devices:', loc='center left', bbox_to_anchor=(1, 0.5))
            plt.xlabel('Time [intervals]')
            plt.ylabel('Power [W]')
            plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
            plt.show()