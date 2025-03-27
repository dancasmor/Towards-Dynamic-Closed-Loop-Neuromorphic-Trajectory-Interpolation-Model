import itertools
import time
import sys
import datetime
import os
from lib.dynapse2_util import set_parameter, clear_srams
from lib.dynapse2_obj import *
from lib.dynapse2_spikegen import *
from lib.dynapse2_raster import *
from lib.dynapse2_network import Network, VirtualGroup
from samna.dynapse2 import *
from custom_util import *


def config_parameters(myConfig, chip):
    # ** CORE 0
    core = 0
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
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DENM_ETAU_P', 1, 40)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DENM_EGAIN_P', 1, 160)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DESC_ITAU_P', 1, 40)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DESC_IGAIN_P', 4, 80)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYAM_W0_P', 5, 250)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYAM_W1_P', 5, 250)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYAM_W2_P', 5, 250)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYAM_W3_P', 5, 250)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYPD_EXT_N', 3, 200)
    # ** END CORE 0

    # ** CORE 1
    core = 1
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
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DENM_ETAU_P', 1, 40)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DENM_EGAIN_P', 1, 160)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DESC_ITAU_P', 1, 40)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DESC_IGAIN_P', 4, 80)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYAM_W0_P', 5, 250)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYAM_W1_P', 5, 250)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYAM_W2_P', 5, 250)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYAM_W3_P', 5, 250)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYPD_EXT_N', 3, 200)
    # ** END CORE 1

    # ** CORE 2
    core = 2
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
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DENM_ETAU_P', 1, 40)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DENM_EGAIN_P', 1, 160)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DESC_ITAU_P', 1, 40)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DESC_IGAIN_P', 4, 80)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYAM_W0_P', 5, 250)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYAM_W1_P', 5, 250)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYAM_W2_P', 5, 250)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYAM_W3_P', 5, 250)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYPD_EXT_N', 3, 200)
    # ** END CORE 2

    # ** CORE 3
    core = 3
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
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DENM_ETAU_P', 1, 40)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DENM_EGAIN_P', 1, 160)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DESC_ITAU_P', 1, 40)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DESC_IGAIN_P', 4, 80)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYAM_W0_P', 5, 250)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYAM_W1_P', 5, 250)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYAM_W2_P', 5, 250)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYAM_W3_P', 5, 250)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYPD_EXT_N', 3, 200)
    # ** END CORE 3


def create_network(network, numNeurons, numPop, chip, core, offset):
    # Create and connect virtual input and ring pop dummy (not working the first neuron/synapse)
    network.add_connection(source=network.add_virtual_group(size=1), target=network.add_group(chip=0, core=0, size=1, name="dummy"),
                           probability=1, dendrite=Dendrite.ampa, weight=[True, True, True, True], repeat=16)

    # Virtual populations
    print("*   Create virtual populations")
    #   * inRefP (input pop for reference position)
    inRefP_pops = [[network.add_virtual_group(size=numNeurons) for _ in range(numPop)] for _ in range(len(core))]
    virtualPops = {"inRefP_pops":inRefP_pops}

    # Create 1 wta network for each joint
    print("*   Create wta networks")
    for id, coreId in enumerate(core):
        create_wta_network(network, numNeurons, numPop, chip, coreId, offset[id%len(offset)], inRefP_pops, id)

    # Create all elements in board and check for problems
    print("*   Insert model on board")
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


def create_wta_network(network, numNeurons, numPop, chip, core, offset, inRefP_pops, jointId):
    # Real populations (wta shifted pops)
    print("*     WTA " + str(jointId))
    #   * outR (outer ring of wta shifted)
    outR_pops = [network.add_group(chip=chip, core=core, size=numNeurons, name="j"+str(jointId)+"outR_" + str(i)) for i in range(numPop)]
    #   * inR (inner ring of wta shifted)
    inR_pops = [network.add_group(chip=chip, core=core, size=numNeurons, name="j"+str(jointId)+"inR_" + str(i)) for i in range(numPop)]

    # Synapses
    for i in range(numPop):
        # inRefP_i - outR_i (exc)
        network.add_connection(source=inRefP_pops[jointId][i], target=outR_pops[i], probability=1, dendrite=Dendrite.ampa,
                               weight=[True, True, True, True], repeat=16)
        # outR_i - inR_i+offset (exc)
        network.add_connection(source=outR_pops[i], target=inR_pops[(i + offset) % numPop], probability=1,
                               dendrite=Dendrite.ampa,
                               weight=[True, True, True, True], repeat=16)
        # inR_i - inR_(All except i) (inh)
        for j in range(numPop):
            if not(i == j):
                # inR_i - inR_j (inh)
                network.add_connection(source=inR_pops[i], target=inR_pops[j], probability=1, dendrite=Dendrite.shunt,
                                       weight=[True, True, True, True], repeat=16)


def experimentation(board, numNeurons, rep, wtimeDExperiment, rtimeBExperiment, wtimeBExperiments, virtualPops, inPosCombs, joints):
    global_events = []
    global_timestamps = []
    t_global = 0
    t_global_exps = []
    inRefP_pops = virtualPops["inRefP_pops"]

    for jointId in range(joints):
        # One experiment for each possible combinations of inputs positions
        for expId, inPosComb in enumerate(inPosCombs):
            print("\n\n\n*** Joint=" + str(jointId) + " experiment" + str(expId) + " refP=" + str(inPosComb["refP"]) + " ***")

            # Define input events
            print("* Create refP events")
            neurons = [i for i in range(numNeurons) for _ in range(rep)]
            timestamps = [r + i * wtimeDExperiment for i in range(numNeurons) for r in range(rep)]

            if not (len(neurons) == len(timestamps)):
                sys.exit("(ERROR) Error to generate events: number of Neurons and Timestamps has to be the same")
            input_events = isi_gen(virtual_group=inRefP_pops[jointId][inPosComb["refP"]], neurons=neurons, timestamps=timestamps)
            print("(DEBUG) Input refP events")
            print("    (id, tag, chip/core, t)")
            print("    " + str(input_events))

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
            t_global = timestamp_formated[len(timestamp_formated) - 1] + wtimeBExperiments

            global_events.append(output_events[0])
            global_timestamps.append(timestamp_formated)

            print("\n*** End Joint=" + str(jointId) + " experiment" + str(expId) + " refP=" + str(inPosComb["refP"]) + " ***")
        t_global_exps.append(t_global)
    return global_events, global_timestamps, t_global_exps


def main(board, number_of_chips, profile_path):
    # * NETWORK parameters
    # Number of populations
    #numPositions = 16
    numPositions = 4
    # Number of neurons of each population
    numNeuronsEachPop = 1
    # Input offset/shift at output
    offset = [1,2,2,1]
    #offset = [3]
    # Only 1 chip is available
    chip = 0
    # There are 4 cores
    core = [0,0,0,0]
    #core = [0]

    # Figure
    save = True
    plot = True
    saveFigPath = "plots/wta/joints"+str(len(core))+"(core="+str(core)+")_ring" + str(numPositions) + "_offset" + str(offset) + "_" + str(datetime.datetime.now()) + ".png"

    # * EXPERIMENTATION parameters
    # Num repetitions of input spikes
    rep = 10
    # Time between experiments (each experiment begins with activation of a different ref positions)
    wtimeBExperiments = 100
    # Reading time during experiment
    rtimeBExperiment = 500
    # Time difference between activation of differents neuron of the same virtual group (same experimentation)
    wtimeDExperiment = 50
    # Inputs combinations to experiments
    #       - Each possible combination of reference position
    inPosCombs = []
    for i in range(numPositions):
        inPosCombs.append({"refP": i})

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
    config_parameters(myConfig=myConfig, chip=chip)
    model.apply_configuration(myConfig)
    time.sleep(0.1)

    # Create the network
    print("* Create networks")
    network = Network(config=myConfig, profile_path=profile_path, num_chips=number_of_chips)
    virtualPops = create_network(network=network, numNeurons=numNeuronsEachPop, numPop=numPositions, chip=chip, core=core,
                                 offset=offset)
    model.apply_configuration(myConfig)
    time.sleep(0.1)

    # Run experimentation
    global_events, global_timestamps, t_global_exps = experimentation(board=board, numNeurons=numNeuronsEachPop,
                                                       rep=rep, wtimeDExperiment=wtimeDExperiment,
                                                       rtimeBExperiment=rtimeBExperiment,
                                                       wtimeBExperiments=wtimeBExperiments,
                                                       virtualPops=virtualPops, inPosCombs=inPosCombs,
                                                       joints=len(core))
    # Get visual data
    path, file = write_file(saveFigPath.replace(".png", ".txt"), "", "",
                            {"global_events": global_events, "global_timestamps": global_timestamps,
                             "t_global_exps": t_global_exps})
    print(path)
    rasterplot_wta(global_events, global_timestamps, numPositions, len(core), t_global_exps,
                            save=save, plot=plot, saveFigPath=saveFigPath)
    #rasterplot(global_events, global_timestamps)
