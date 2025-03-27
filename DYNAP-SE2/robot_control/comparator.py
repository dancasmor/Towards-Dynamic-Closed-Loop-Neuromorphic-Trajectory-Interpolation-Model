import itertools
import time
import sys
import os
from lib.dynapse2_util import set_parameter, clear_srams
from lib.dynapse2_obj import *
from lib.dynapse2_spikegen import *
from lib.dynapse2_raster import *
from lib.dynapse2_network import Network, VirtualGroup
from samna.dynapse2 import *
from custom_util import *
import datetime

def config_parameters(myConfig, chip, core):
    # Set global parameters for the chip
    set_parameter(myConfig.chips[chip].shared_parameters01, "PG_BUF_N", 0, 100)
    set_parameter(myConfig.chips[chip].shared_parameters23, "PG_BUF_N", 0, 100)

    # Set core parameters
    #   * Neuron
    set_parameter(myConfig.chips[chip].cores[core].parameters, "SOIF_GAIN_N", 3, 80)
    set_parameter(myConfig.chips[chip].cores[core].parameters, "SOIF_LEAK_N", 0, 50)
    set_parameter(myConfig.chips[chip].cores[core].parameters, "SOIF_REFR_N", 2, 250)
    set_parameter(myConfig.chips[chip].cores[core].parameters, "SOIF_DC_P", 0, 1)
    set_parameter(myConfig.chips[chip].cores[core].parameters, "SOIF_SPKTHR_P", 3, 254)
    #   * Synapse
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DEAM_ETAU_P', 2, 40)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DEAM_EGAIN_P', 4, 80)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DENM_ETAU_P', 2, 40)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DENM_EGAIN_P', 4, 80)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DEGA_ITAU_P', 2, 5)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DEGA_IGAIN_P', 2, 40)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DESC_ITAU_P', 2, 40)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DESC_IGAIN_P', 0, 20)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYAM_W0_P', 5, 250)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYAM_W1_P', 5, 250)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYAM_W2_P', 5, 250)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYAM_W3_P', 5, 250)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYPD_EXT_N', 3, 200)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYPD_DLY0_P', 2, 200)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYPD_DLY1_P', 5, 200)


def create_network(network, numNeurons, numPop, chip, core):
    # Create and connect virtual input and ring pop dummy (not working the first neuron/synapse)
    network.add_connection(source=network.add_virtual_group(size=1), target=network.add_group(chip=0, core=core, size=1, name="dummy"),
                           probability=1, dendrite=Dendrite.ampa, weight=[True, True, True, True], repeat=16)

    # Virtual populations
    #   * inRobP (input pop for robot position)
    inRobP_pops = [network.add_virtual_group(size=numNeurons) for _ in range(numPop)]
    #   * inRefP (input pop for reference position)
    inRefP_pops = [network.add_virtual_group(size=numNeurons) for _ in range(numPop)]
    virtualPops = {"inRobP_pops":inRobP_pops, "inRefP_pops":inRefP_pops}

    # Real populations (comparator pops)
    #   * cmpRobP (robot position neuron in comparator)
    cmpRobP_pops = [network.add_group(chip=chip, core=core, size=numNeurons, name="cmprobp_"+str(i)) for i in range(numPop)]
    #   * cmpRefP (reference position neuron in comparator)
    cmpRefP_pops = [network.add_group(chip=chip, core=core, size=numNeurons, name="cmprefp_" + str(i)) for i in range(numPop)]
    #   * lInh (local inhibition neuron in comparator)
    lInh_pops = [network.add_group(chip=chip, core=core, size=numNeurons, name="linh_" + str(i)) for i in range(numPop)]
    #   * cmpOut (output signal of comparator)
    cmpOut_pops = [network.add_group(chip=chip, core=core, size=numNeurons, name="cmpout_" + str(i)) for i in range(numPop)]

    # Synapses
    for i in range(numPop):
        # inRobP_i - cmpRobP_i (exc)
        network.add_connection(source=inRobP_pops[i], target=cmpRobP_pops[i], probability=1, dendrite=Dendrite.nmda,
                               weight=[True, True, True, True], repeat=16)
        # inRefP - cmpRefp_i (exc)
        network.add_connection(source=inRefP_pops[i], target=cmpRefP_pops[i], probability=1, dendrite=Dendrite.nmda,
                               weight=[True, True, True, True], repeat=16)
        # inRobP_i - lInh_i (exc)
        network.add_connection(source=inRobP_pops[i], target=lInh_pops[i], probability=1, dendrite=Dendrite.ampa,
                               weight=[True, True, True, True], repeat=16)
        # inRefP - lInh_i (exc)
        network.add_connection(source=inRefP_pops[i], target=lInh_pops[i], probability=1, dendrite=Dendrite.ampa,
                               weight=[True, True, True, True], repeat=16)
        # cmpRobP_i - cmpOut_i (exc)
        network.add_connection(source=cmpRobP_pops[i], target=cmpOut_pops[i], probability=1, dendrite=Dendrite.nmda,
                               weight=[True, True, True, True], repeat=16)
        # cmpRefP_i - cmpOut_i (exc)
        network.add_connection(source=cmpRefP_pops[i], target=cmpOut_pops[i], probability=1, dendrite=Dendrite.nmda,
                               weight=[True, True, True, True], repeat=16)
        # lInh_i - cmpOut_i (inh)
        network.add_connection(source=lInh_pops[i], target=cmpOut_pops[i], probability=1, dendrite=Dendrite.gaba,
                               weight=[True, True, True, True], repeat=16, precise_delay=True, mismatched_delay=False)

        network.add_connection(source=lInh_pops[i], target=cmpOut_pops[i], probability=1, dendrite=Dendrite.shunt,
                               weight=[True, False, False, False], repeat=16)

    # Create all elements in board and check for problems
    network.connect()
    # Debug information of the network
    print("(DEBUG) Virtual populations")
    for pop in network.virtual_groups:
        print("  " + str(pop.get_ids()) + " destinations=" + str(pop.get_destinations()))
    print("(DEBUG) Populations")
    for pop in network.groups:
        print("  " + str(pop.name) + " neurons=" + str(pop.neurons) + " ids=" + str(pop.ids) + " destinations=" + str(pop.destinations))
    print("(DEBUG) Synapses")
    for syn in network.connections:
        if type(syn.source) is VirtualGroup:
            print("  " + "Virtual-" + str(syn.target.name) + " (" + str(syn.dendrite) + ")")
        else:
            print("  " + str(syn.source.name) + "-" + str(syn.target.name) + " (" + str(syn.dendrite) + ")")
    return virtualPops


def experimentation(board, numNeurons, rep, wtimeDExperiment, rtimeBExperiment, wtimeBExperiments, virtualPops, inPosCombs):
    global_events = []
    global_timestamps = []
    t_global = 0
    inRobP_pops = virtualPops["inRobP_pops"]
    inRefP_pops = virtualPops["inRefP_pops"]

    # One experiment for each possible combinations of inputs positions
    for expId, inPosComb in enumerate(inPosCombs):
        print("\n\n\n*** Experiment " + str(expId) + " robP=" + str(inPosComb["robP"]) + " refP=" + str(inPosComb["refP"]) + " ***")

        # Define input events
        print("* Create robP events")
        if not(inPosComb["robP"] == -1):
            neurons = [i for i in range(numNeurons) for _ in range(rep)]
            timestamps = [r + i * wtimeDExperiment for i in range(numNeurons) for r in range(rep)]

            if not (len(neurons) == len(timestamps)):
                sys.exit("(ERROR) Error to generate events: number of Neurons and Timestamps has to be the same")
            input_events = isi_gen(virtual_group=inRobP_pops[inPosComb["robP"]], neurons=neurons, timestamps=timestamps)
            print("(DEBUG) Input robP events")
            print("    (id, tag, chip/core, t)")
            print("    " + str(input_events))
        else:
            input_events = []
            print("(DEBUG) Input robP events")
            print("    (id, tag, chip/core, t)")
            print("    None")

        print("* Create refP events")
        if not (inPosComb["refP"] == -1):
            neurons = [i for i in range(numNeurons) for _ in range(rep)]
            timestamps = [r + i * wtimeDExperiment for i in range(numNeurons) for r in range(rep)]

            if not (len(neurons) == len(timestamps)):
                sys.exit("(ERROR) Error to generate events: number of Neurons and Timestamps has to be the same")
            input_events = input_events + (isi_gen(virtual_group=inRefP_pops[inPosComb["refP"]], neurons=neurons, timestamps=timestamps))
            print("(DEBUG) Input refP events")
            print("    (id, tag, chip/core, t)")
            print("    " + str(input_events))
        else:
            print("(DEBUG) Input refP events")
            print("    (id, tag, chip/core, t)")
            print("    None")


        # Collect and discard random events
        print("* Dump random events")
        output_events = [[], []]
        get_events(board=board, extra_time=1000, output_events=output_events, blocking=False)
        print(output_events)

        # Send inputs events from opall kelly
        print("* Send input events")
        ts = get_fpga_time(board=board) + 1000000
        send_virtual_events(board=board, virtual_events=input_events, offset=ts, min_delay=500000)

        # Get output events
        print("* Get output events")
        """
            extra_time = get output after x ms since first output event (blocking)
            blocking = if FALSE get output after x ms regardless of whether or not there is an event (not blocking)
        """
        output_events = [[], []]
        get_events(board=board, extra_time=rtimeBExperiment, output_events=output_events)
        print("(DEBUG) Output events")
        t_offset = 0
        timestamp_formated = []
        for id, t in zip(output_events[0], output_events[1]):
            if t_offset == 0:
                t_offset = t
            t = int((t - t_offset) * 1e3) + t_global
            print("  t=" + str(t) + " id=" + str(id))
            timestamp_formated.append(t)
        if len(timestamp_formated) == 0:
            print("  NO output events")

        if not (inPosComb["robP"] == -1 and inPosComb["refP"] == -1):
            t_global = timestamp_formated[len(timestamp_formated) - 1] + wtimeBExperiments

            global_events.append(output_events[0])
            global_timestamps.append(timestamp_formated)
        print("*** End of experiment " + str(expId) + " robP=" + str(inPosComb["robP"]) + " refP=" + str(inPosComb["refP"]) + " ***")
    return global_events, global_timestamps


def main(board, number_of_chips, profile_path):
    # * NETWORK parameters
    # Number of populations
    numPositions = 4
    # Number of neurons of each population
    numNeuronsEachPop = 1
    # Only 1 chip is available
    chip = 0
    # There are 4 cores
    core = 2

    # Figure
    save = True
    plot = True
    saveFigPath = "plots/comparator/comparator_core"+str(core)+"/comparator_"+str(numPositions)+"pos_rasterplot_"+str(datetime.datetime.now())+".png"

    # * EXPERIMENTATION parameters
    # Num repetitions of input spikes
    rep = 10
    # Time between experiments (each experiment begins with activation of a different pair of robot and reference positions)
    wtimeBExperiments = 100
    # Reading time during experiment
    rtimeBExperiment = 500
    # Time difference between activation of differents neuron of the same virtual group (same experimentation)
    wtimeDExperiment = 50
    # Inputs combinations to experiments
    #       - Each possible combination (including only 1 input: ref or rob = -1)
    inPosCombs = []
    for i in range(-1, numPositions):
        for j in range(-1, numPositions):
            inPosCombs.append({"robP": i, "refP": j})

    # Create a new network model and reset it
    model = board.get_model()
    model.reset(ResetType.PowerCycle, 0b1)
    time.sleep(1)

    # Default configuration
    myConfig = model.get_configuration()
    model.apply_configuration(myConfig)
    time.sleep(1)

    # Define configuration for core 0
    print("* Apply configuration")
    config_parameters(myConfig=myConfig, chip=chip, core=core)
    model.apply_configuration(myConfig)
    time.sleep(0.1)

    # Create the network
    print("* Create networks")
    network = Network(config=myConfig, profile_path=profile_path, num_chips=number_of_chips)
    virtualPops = create_network(network=network, numNeurons=numNeuronsEachPop, numPop=numPositions, chip=chip, core=core)
    model.apply_configuration(myConfig)
    time.sleep(0.1)

    # Run experimentation
    global_events, global_timestamps = experimentation(board=board, numNeurons=numNeuronsEachPop,
                                                       rep=rep, wtimeDExperiment=wtimeDExperiment,
                                                       rtimeBExperiment=rtimeBExperiment,
                                                       wtimeBExperiments=wtimeBExperiments,
                                                       virtualPops=virtualPops, inPosCombs=inPosCombs)
    # Get visual data
    path, file = write_file(saveFigPath.replace(".png", ".txt"), "", "", {"global_events": global_events, "global_timestamps": global_timestamps})
    print(path)
    rasterplot_comparator(global_events, global_timestamps, numPositions, save=save, plot=plot, saveFigPath=saveFigPath)
