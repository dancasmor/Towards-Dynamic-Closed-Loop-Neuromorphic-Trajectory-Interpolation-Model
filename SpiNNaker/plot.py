
import matplotlib.pyplot as plt
import matplotlib.ticker as MaxNLocator
import numpy as np

def rasterplot(spikes, save=False, plot=True, saveFigPath=False):
    #plt.figure(figsize=(26, 29))
    plt.figure()

    plt.gca().xaxis.set_major_locator(MaxNLocator.MaxNLocator(integer=True))

    populationsXValues = []
    populationsYValues = []
    globalIndex = 0
    for name, populationSpikes in spikes.items():
        xvalues = []
        yvalues = []
        # Assign y value (population index) and y label
        for indexNeuron, spikesSingleNeuron in enumerate(populationSpikes):
            xvalues = xvalues + spikesSingleNeuron
            yvalues = yvalues + [indexNeuron + globalIndex for _ in spikesSingleNeuron]
        globalIndex = globalIndex + len(populationSpikes)
        # Add to the populations values list
        populationsXValues.append(xvalues)
        populationsYValues.append(yvalues)

    # Add a horizontal line to separate the output and input neurons from others
    plt.axhline(y=4 - 0.5, color='r', linestyle='-', alpha=0.2)
    plt.axhline(y=8 - 0.5, color='r', linestyle='-', alpha=0.2)
    # Add spikes to scatterplot
    for indexPop in range(len(spikes)):
        plt.plot(populationsXValues[indexPop], populationsYValues[indexPop], "o", markersize=2, color="black")

    plt.ylabel("Neuron ID")
    plt.xlabel("Time (ms)")
    if save:
        plt.savefig(saveFigPath)
    if plot:
        plt.show()
    plt.close()

def rasterplot_comparator(spikes, experimentSize, timeExpLimit, save=False, plot=True, saveFigPath=False):
    plt.figure(figsize=(31, 29))
    colors = ["blue", "green", "orange", "black", "darkviolet"]
    alpha = 0.2
    fontsize = 30
    markersize = 6

    # Insert the first case where no ref and no rob positions
    xValues = []
    yValues = []
    globalIndex = 0
    for name, populationSpikes in spikes.items():
        # Assign y value (population index) and y label
        for indexNeuron, spikesSingleNeuron in enumerate(populationSpikes):
            xValues = xValues + spikesSingleNeuron
            yValues = yValues + [indexNeuron + globalIndex for _ in spikesSingleNeuron]
        globalIndex = globalIndex + len(populationSpikes)

    outNeuronLimit = experimentSize*5-1
    inNeuronLimit = experimentSize*2-1
    experimentSize = experimentSize+1

    # Format the spikes and timestamp to group by experiment case
    neuronsFormated = [[] for i in range(experimentSize)]
    timestampsFormated = [[] for i in range(experimentSize)]
    for i in range(len(timeExpLimit)):
        if i == len(timeExpLimit)-1:
            break
        for xIndex, x in enumerate(xValues):
            if int(x) >= timeExpLimit[i] and int(x) <= timeExpLimit[i+1]:
                neuronsFormated[i].append(yValues[xIndex])
                timestampsFormated[i].append(x)

    # Plot the spikes
    plt.plot([], [], '^', markersize=markersize + 1, color="r", label="cmpOUT")
    for i in range(len(neuronsFormated)):
        plt.plot(timestampsFormated[i], neuronsFormated[i], 'o', markersize=markersize, color=colors[i%len(colors)], label="ref=rob="+str(i))
        # Mark output neurons
        if not(i==0):
            indices = [index for index, element in enumerate(neuronsFormated[i]) if (element == outNeuronLimit+i)]
            selectedNeurons = [outNeuronLimit+i for index in indices]
            selectedTimestamps = [timestampsFormated[i][index] for index in indices]
            plt.plot(selectedTimestamps, selectedNeurons, '^', markersize=markersize + 1, color="r")

    for timeLimit in timeExpLimit[1:len(timeExpLimit)-1]:
        # Add vertical line to separate experiment cases
        plt.axvline(x=timeLimit, color='r', alpha=alpha)
    # Add a horizontal line to separate the output and input neurons from others
    plt.axhline(y=outNeuronLimit+0.5, color='r', linestyle='-', alpha=alpha)
    plt.axhline(y=inNeuronLimit+0.5, color='r', linestyle='-', alpha=alpha)

    plt.ylabel("Neuron ID", fontsize=fontsize)
    plt.xlabel("Time (ms)", fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.xticks(fontsize=fontsize)

    plt.legend(bbox_to_anchor=(1.0, 0.95), loc='upper left', fontsize=fontsize)
    #plt.tight_layout()

    if save:
        plt.savefig(saveFigPath)
    if plot:
        plt.show()
    plt.close()

def rasterplot_full_network_separate_inputs(spikes, coarseGrainPositions, fineGrainPositions, save=False, plot=True, saveFigPath=False):
    plt.figure(figsize=(26, 29))
    alpha = 0.28
    fontsize = 30
    markersize = 4

    inCoarseLimit = coarseGrainPositions
    inFineLimit = inCoarseLimit + fineGrainPositions
    inRefLimit = inFineLimit + coarseGrainPositions
    wtaLimit = inRefLimit + 2*coarseGrainPositions
    cmpCoarseLimit = wtaLimit + 4*coarseGrainPositions
    cmpFineLimit = cmpCoarseLimit + 1
    signalCmpOutNeuron = cmpFineLimit + 3


    populationsXValues = []
    populationsYValues = []
    globalIndex = 0
    for name, populationSpikes in spikes.items():
        xvalues = []
        yvalues = []
        # Assign y value (population index) and y label
        for indexNeuron, spikesSingleNeuron in enumerate(populationSpikes):
            xvalues = xvalues + spikesSingleNeuron
            yvalues = yvalues + [indexNeuron + globalIndex for _ in spikesSingleNeuron]
        globalIndex = globalIndex + len(populationSpikes)
        # Add to the populations values list
        populationsXValues.append(xvalues)
        populationsYValues.append(yvalues)

    # Plot the spikes
    for i in range(len(populationsYValues)):
        plt.plot(populationsXValues[i], populationsYValues[i], 'o', markersize=markersize, color="black")
        # Select cmp out signal neuron
        if signalCmpOutNeuron in populationsYValues[i]:
            indices = [index for index, element in enumerate(populationsYValues[i]) if (element == signalCmpOutNeuron)]
            selectedNeurons = [signalCmpOutNeuron for _ in indices]
            selectedTimestamps = [populationsXValues[i][index] for index in indices]
            plt.plot(selectedTimestamps, selectedNeurons, '^', markersize=markersize+2, color="red", label="out_signal")

    # Add red horizontal line to separate main components
    plt.axhline(y=inCoarseLimit - 0.5, color='r', linestyle='-', alpha=alpha)
    plt.axhline(y=inFineLimit - 0.5, color='r', linestyle='-', alpha=alpha)
    plt.axhline(y=inRefLimit - 0.5, color='r', linestyle='-', alpha=alpha)
    plt.axhline(y=wtaLimit - 0.5, color='r', linestyle='-', alpha=alpha)
    plt.axhline(y=cmpCoarseLimit - 0.5, color='r', linestyle='-', alpha=alpha)
    plt.axhline(y=cmpFineLimit - 0.5, color='r', linestyle='-', alpha=alpha)
    # Add green horizontal line to separate different parts of the same component
    wtaOutRLimit = inRefLimit + coarseGrainPositions
    cmpCoarseRobLimit = wtaLimit + coarseGrainPositions
    cmpCoarseRefLimit = cmpCoarseRobLimit + coarseGrainPositions
    cmpCoarseInhLimit = cmpCoarseRefLimit + coarseGrainPositions
    cmpOutInLimit = cmpFineLimit + 1
    cmpOutcmpLimit = cmpOutInLimit + 1
    cmpOutInhLimit = cmpOutcmpLimit + 1
    plt.axhline(y=wtaOutRLimit - 0.5, color='g', linestyle='-', alpha=alpha)
    plt.axhline(y=cmpCoarseRobLimit - 0.5, color='g', linestyle='-', alpha=alpha)
    plt.axhline(y=cmpCoarseRefLimit - 0.5, color='g', linestyle='-', alpha=alpha)
    plt.axhline(y=cmpCoarseInhLimit - 0.5, color='g', linestyle='-', alpha=alpha)
    plt.axhline(y=cmpOutInLimit - 0.5, color='g', linestyle='-', alpha=alpha)
    plt.axhline(y=cmpOutcmpLimit - 0.5, color='g', linestyle='-', alpha=alpha)
    plt.axhline(y=cmpOutInhLimit - 0.5, color='g', linestyle='-', alpha=alpha)

    plt.ylabel("Neuron ID", fontsize=fontsize)
    plt.xlabel("Time (ms)", fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.xticks(fontsize=fontsize)

    #plt.ylim([0, signalCmpOutNeuron+1])
    plt.ylim([-1, signalCmpOutNeuron + 4])

    # plt.legend(bbox_to_anchor=(1.0, 0.95), loc='upper left')
    # plt.tight_layout()

    if save:
        plt.savefig(saveFigPath)
    if plot:
        plt.show()
    plt.close()

# Plot the spike information
def spikes_plot(spikes, popNames, pointTypes, colors, title, outFilePath, baseFilename, plot, write,
                figsize, linesMark, alphaLinesMark, spikesPointSize, fontsize, labelsize, alternateXtick, defaultXtick):
    if not figsize:
        plt.figure()
    else:
        plt.figure(figsize=figsize)

    if not colors:
        colors = list(plt.cm.jet(np.linspace(0,1,len(popNames))))

    # Add point for each neuron of each population that fire, take y labels and x labels
    populationsXValues = []
    populationsYValues = []
    globalIndex = 0
    listYticks = []
    listXticks = []
    for indexPop, populationSpikes in enumerate(spikes):
        xvalues = []
        yvalues = []
        # Assign y value (population index) and y label
        for indexNeuron, spikesSingleNeuron in enumerate(populationSpikes):
            listYticks.append(popNames[indexPop] + str(indexNeuron))
            xvalues = xvalues + spikesSingleNeuron
            yvalues = yvalues + [indexNeuron + globalIndex for _ in spikesSingleNeuron]
        globalIndex = globalIndex + len(populationSpikes)
        # Add to the populations values list
        populationsXValues.append(xvalues)
        populationsYValues.append(yvalues)
        # Add xvalues to labels
        listXticks = list(set(listXticks + xvalues))
    maxXvalue = max(listXticks)
    minXvalue = min(listXticks)

    # Lines for each points
    if linesMark:
        for indexPop in range(len(spikes)):
            plt.vlines(populationsXValues[indexPop], ymin=-1, ymax=populationsYValues[indexPop], color=colors[indexPop%len(colors)],
                       alpha=alphaLinesMark)
            plt.hlines(populationsYValues[indexPop], xmin=-1, xmax=populationsXValues[indexPop], color=colors[indexPop%len(colors)],
                       alpha=alphaLinesMark)

    # Add spikes to scatterplot
    for indexPop in range(len(spikes)):
        plt.plot(populationsXValues[indexPop], populationsYValues[indexPop], pointTypes[indexPop],
                 color=colors[indexPop%len(colors)], label=popNames[indexPop], markersize=spikesPointSize)

    # Metadata
    plt.xlabel("Simulation time (ms)", fontsize=fontsize)
    plt.ylabel("Neuron spikes", fontsize=fontsize)
    plt.title(title, fontsize=fontsize)
    plt.ylim([-1, globalIndex])
    plt.yticks(range(len(listYticks)), listYticks, fontsize=labelsize)
    plt.legend(fontsize=fontsize)


    if alternateXtick:
        # Divide xticks list in pair or odd position
        listXticks.sort()
        listXticksOdd = [int(tick) for index, tick in enumerate(listXticks) if not (index % 2 == 0)]
        listXticksPair = [int(tick) for index, tick in enumerate(listXticks) if index % 2 == 0]
        # Write them with alternate distance
        ax = plt.gca()
        ax.set_xticklabels(listXticksOdd, minor=True)
        ax.set_xticks(listXticksOdd, minor=True)
        ax.set_xticklabels(listXticksPair, minor=False)
        ax.set_xticks(listXticksPair, minor=False)
        ax.tick_params(axis='x', which='minor', pad=35)
        ax.tick_params(axis='x', which='both', labelsize=labelsize, rotation=90)
        plt.xlim(minXvalue - 1, maxXvalue + 1)
    else:
        if defaultXtick:
            plt.yticks(fontsize=labelsize)
        else:
            plt.yticks(range(len(listXticks)), listXticks, fontsize=labelsize)

    plt.legend(fontsize=fontsize, bbox_to_anchor=(1.0, 0.95), loc='upper left')

    plt.tight_layout()

    # Save and/or plot
    if write:
        plt.savefig(outFilePath + baseFilename + ".png")
    if plot:
        plt.show()
    plt.close()