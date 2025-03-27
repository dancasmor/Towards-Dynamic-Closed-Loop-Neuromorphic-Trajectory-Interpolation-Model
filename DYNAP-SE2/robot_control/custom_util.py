
import matplotlib.pyplot as plt


def write_file(basePath, filename, extension, data):
    # Generic function to write the data into a file
    file = open(basePath + filename + extension, "w")
    file.write(str(data))
    file.close()
    return basePath + filename + extension, filename


def read_file(basePath, filename, extension):
    # Generic function to write the data into a file
    file = open(basePath + filename + extension, "r")
    data = file.read()
    file.close()
    return data


def rasterplot(neurons, timestamps, save=False, plot=True, saveFigPath=False):
    plt.figure(figsize=(26, 29))
    for i in range(len(neurons)):
        plt.plot(timestamps[i], neurons[i], 'o', markersize=2)
    plt.ylabel("Neuron ID")
    plt.xlabel("Time (ms)")
    if save:
        plt.savefig(saveFigPath)
    if plot:
        plt.show()
    plt.close()

def rasterplot_comparator(neurons, timestamps, experimentSize, save=False, plot=True, saveFigPath=False):
    plt.figure(figsize=(31, 29))
    #colors = ["green", "orange", "black", "peru", "tan", "gold", "lightcoral", "violet", "indigo", "#81A74F", "navy", "teal", "aqua", "#E92F74", "darkviolet", "blue", "turquoise"]
    colors = ["blue", "green", "orange", "black", "darkviolet"]
    alpha = 0.2
    fontsize = 30
    markersize = 6

    # Insert the first case where no ref and no rob positions
    neurons.insert(0, [])
    timestamps.insert(0, [])
    outNeuronLimit = experimentSize*5+1
    inNeuronLimit = experimentSize*2+1
    experimentSize = experimentSize+1

    # Format the spikes and timestamp to group by experiment case
    neuronsFormated = [[] for i in range(experimentSize)]
    timestampsFormated = [[] for i in range(experimentSize)]
    for i in range(len(neurons)):
        neuronsFormated[i//experimentSize] = neuronsFormated[i//experimentSize] + neurons[i]
        timestampsFormated[i//experimentSize] = timestampsFormated[i//experimentSize] + timestamps[i]

    # Plot the spikes
    firstOut = True
    plt.plot([], [], '^', markersize=markersize + 1, color="r", label="cmpOUT")
    for i in range(len(neuronsFormated)):
        plt.plot(timestampsFormated[i], neuronsFormated[i], 'o', markersize=markersize, color=colors[i%len(colors)], label="ref=rob="+str(i))
        # Add vertical line to separate experiment cases
        if not(i == len(neuronsFormated)-1):
            plt.axvline(x=timestampsFormated[i][len(timestampsFormated[i])-1]+50, color='r', alpha=alpha)
        # Mark output neurons
        if not(i==0):
            indices = [index for index, element in enumerate(neuronsFormated[i]) if (element == outNeuronLimit+i)]
            selectedNeurons = [outNeuronLimit+i for index in indices]
            selectedTimestamps = [timestampsFormated[i][index] for index in indices]
            plt.plot(selectedTimestamps, selectedNeurons, '^', markersize=markersize + 1, color="r")

        # Add a horizontal line to separate the output and input neurons from others
    plt.axhline(y=outNeuronLimit+0.5, color='r', linestyle='-', alpha=alpha)
    plt.axhline(y=inNeuronLimit + 0.5, color='r', linestyle='-', alpha=alpha)

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


def rasterplot_wta(neurons, timestamps, numPositions, numJoints, t_global_exps, save, plot, saveFigPath):
    plt.figure(figsize=(26, 29))
    alpha = 0.2
    fontsize = 30
    markersize = 6

    # Insert the first case where no ref and no rob positions
    neurons.insert(0, [])
    timestamps.insert(0, [])

    # Plot the spikes
    for i in range(len(neurons)):
        plt.plot(timestamps[i], neurons[i], 'o', markersize=markersize, color='black')

    # Add a horizontal line to separate the output and input neurons from others
    inNeuronLimit = numPositions * numJoints
    plt.axhline(y=inNeuronLimit + 1.0, color='r', linestyle='-', alpha=alpha)
    lastJointLimit = inNeuronLimit+1
    for jointId in range(numJoints):
        inLocalNeuronLimit = numPositions * (jointId+1)
        outRingLimit = lastJointLimit + numPositions
        inRingLimit = outRingLimit + numPositions
        plt.axhline(y=outRingLimit + 0.5, color='r', linestyle='-', alpha=alpha)
        if not(jointId+1 == numJoints):
            plt.axhline(y=inLocalNeuronLimit + 0.5, color='r', linestyle='-', alpha=alpha)
            plt.axhline(y=inRingLimit + 0.5, color='r', linestyle='-', alpha=alpha)
        lastJointLimit = inRingLimit

    # Add vertical line to separate different wta networks
    for id, t_global in enumerate(t_global_exps):
        if not(id+1 == len(t_global_exps)):
            plt.axvline(x=t_global - 50, color='r', linestyle='-', alpha=alpha)

    plt.ylabel("Neuron ID", fontsize=fontsize)
    plt.xlabel("Time (ms)", fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.xticks(fontsize=fontsize)

    #plt.legend(bbox_to_anchor=(1.0, 0.95), loc='upper left', fontsize=20)
    # plt.tight_layout()

    if save:
        plt.savefig(saveFigPath)
    if plot:
        plt.show()
    plt.close()


def rasterplot_full_network(neurons, timestamps, coarseGrainPositions, fineGrainPositions, save, plot, saveFigPath):
    plt.figure(figsize=(26, 29))
    colors = ["green", "orange", "black", "peru", "tan", "gold", "lightcoral", "violet", "indigo", "#81A74F", "navy",
              "teal", "aqua", "#E92F74", "darkviolet", "blue", "turquoise"]

    # Insert the first case where no ref and no rob positions
    neurons.insert(0, [])
    timestamps.insert(0, [])
    inNeuronLimit = coarseGrainPositions * fineGrainPositions + coarseGrainPositions + 1
    wtaLimit = inNeuronLimit + coarseGrainPositions * 2
    cmpCoarseLimit = wtaLimit + coarseGrainPositions * 4
    cmpFineLimit = cmpCoarseLimit + 1
    cmpOutLimit = cmpFineLimit + 6

    # Plot the spikes
    for i in range(len(neurons)):
        plt.plot(timestamps[i], neurons[i], 'o', markersize=2)

    # Add a horizontal line to separate the output and input neurons from others
    plt.axhline(y=inNeuronLimit + 0.5, color='r', linestyle='-')
    plt.axhline(y=wtaLimit + 0.5, color='r', linestyle='-')
    plt.axhline(y=cmpCoarseLimit + 0.5, color='r', linestyle='-')
    plt.axhline(y=cmpFineLimit + 0.5, color='r', linestyle='-')
    plt.axhline(y=cmpOutLimit - 1.5, color='r', linestyle='-')

    plt.ylabel("Neuron ID")
    plt.xlabel("Time (ms)")

    plt.legend(bbox_to_anchor=(1.0, 0.95), loc='upper left')
    # plt.tight_layout()

    if save:
        plt.savefig(saveFigPath)
    if plot:
        plt.show()
    plt.close()


def rasterplot_full_network_separate_inputs(neurons, timestamps, coarseGrainPositions, fineGrainPositions, save, plot, saveFigPath):
    plt.figure(figsize=(26, 29))
    alpha = 0.35
    fontsize = 30
    markersize = 4

    # Insert the first case where no ref and no rob positions
    neurons.insert(0, [])
    timestamps.insert(0, [])
    inCoarseLimit = coarseGrainPositions
    inFineLimit = inCoarseLimit + fineGrainPositions
    inRefLimit = inFineLimit + coarseGrainPositions
    wtaLimit = inRefLimit + 2*coarseGrainPositions + 1
    cmpCoarseLimit = wtaLimit + 4* coarseGrainPositions
    cmpFineLimit = cmpCoarseLimit + 1
    signalCmpOutNeuron = cmpFineLimit + coarseGrainPositions + 2

    # Plot the spikes
    for i in range(len(neurons)):
        plt.plot(timestamps[i], neurons[i], 'o', markersize=markersize, color="black")
        # Select cmp out signal neuron
        if signalCmpOutNeuron in neurons[i]:
            indices = [index for index, element in enumerate(neurons[i]) if (element == signalCmpOutNeuron)]
            selectedNeurons = [signalCmpOutNeuron for _ in indices]
            selectedTimestamps = [timestamps[i][index] for index in indices]
            plt.plot(selectedTimestamps, selectedNeurons, '^', markersize=markersize+2, color="red", label="out_signal")

    # Add red horizontal line to separate main components
    plt.axhline(y=inCoarseLimit + 0.5, color='r', linestyle='-', alpha=alpha)
    plt.axhline(y=inFineLimit + 0.5, color='r', linestyle='-', alpha=alpha)
    plt.axhline(y=inRefLimit + 1.0, color='r', linestyle='-', alpha=alpha)
    plt.axhline(y=wtaLimit + 0.5, color='r', linestyle='-', alpha=alpha)
    plt.axhline(y=cmpCoarseLimit + 0.5, color='r', linestyle='-', alpha=alpha)
    plt.axhline(y=cmpFineLimit + 0.5, color='r', linestyle='-', alpha=alpha)
    # Add green horizontal line to separate different parts of the same component
    wtaOutRLimit = inRefLimit + coarseGrainPositions + 1
    cmpCoarseRobLimit = wtaLimit + coarseGrainPositions
    cmpCoarseRefLimit = cmpCoarseRobLimit + coarseGrainPositions
    cmpCoarseInhLimit = cmpCoarseRefLimit + coarseGrainPositions
    cmpOutInLimit = cmpFineLimit + 2
    cmpOutcmpLimit = cmpOutInLimit + 2
    cmpOutInhLimit = cmpOutcmpLimit + 1
    plt.axhline(y=wtaOutRLimit + 0.5, color='g', linestyle='-', alpha=alpha)
    plt.axhline(y=cmpCoarseRobLimit + 0.5, color='g', linestyle='-', alpha=alpha)
    plt.axhline(y=cmpCoarseRefLimit + 0.5, color='g', linestyle='-', alpha=alpha)
    plt.axhline(y=cmpCoarseInhLimit + 0.5, color='g', linestyle='-', alpha=alpha)
    plt.axhline(y=cmpOutInLimit + 0.5, color='g', linestyle='-', alpha=alpha)
    plt.axhline(y=cmpOutcmpLimit + 0.5, color='g', linestyle='-', alpha=alpha)
    plt.axhline(y=cmpOutInhLimit + 0.5, color='g', linestyle='-', alpha=alpha)

    plt.ylabel("Neuron ID", fontsize=fontsize)
    plt.xlabel("Time (ms)", fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.xticks(fontsize=fontsize)

    #plt.ylim([0, signalCmpOutNeuron+1])
    plt.ylim([0, signalCmpOutNeuron + 4])

    # plt.legend(bbox_to_anchor=(1.0, 0.95), loc='upper left')
    # plt.tight_layout()

    if save:
        plt.savefig(saveFigPath)
    if plot:
        plt.show()
    plt.close()