
import time
import sys
import os
import datetime
import math
from lib.dynapse2_util import set_parameter, clear_srams
from lib.dynapse2_obj import *
from lib.dynapse2_spikegen import *
from lib.dynapse2_raster import *
from lib.dynapse2_network import Network, VirtualGroup
from samna.dynapse2 import *
from custom_util import *


def main(board, number_of_chips, profile_path):
    # * NETWORK parameters
    # Num of coarse grain positions
    coarseGrainPositions = 4
    # Num of fine grain positions
    fineGrainPositions = 4
    # Number of neurons of each population
    numNeuronsEachPop = 1
    # Offset of wta
    offset = 1
    # Fine grain position to activate signal
    fineGrainThreshold = math.ceil(fineGrainPositions/2) - 1
    # Only 1 chip is available
    chip = 0

    # Figure
    save = True
    plot = True
    saveFigPath = "plots/full_network/full_network_separate_inputs/coarseGrain"+str(coarseGrainPositions)+"_fineGrain"+str(fineGrainPositions)+"_"+str(datetime.datetime.now())+".png"

    # * EXPERIMENTATION parameters
    # Num repetitions of input spikes
    rep = 10
    # Time between experiments (each experiment begins with activation of a different pair of robot and reference positions)
    wtimeBExperiments = 100
    # Reading time during experiment
    rtimeBExperiment = 500
    # Time difference between activation of differents neuron of the same virtual group (same experimentation)
    wtimeDExperiment = 50

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
    virtualPops = create_network(network=network, coarseGrainPositions=coarseGrainPositions,
                                 fineGrainPositions=fineGrainPositions, numNeurons=numNeuronsEachPop, chip=chip,
                                 offset=offset, fineGrainThreshold=fineGrainThreshold)
    model.apply_configuration(myConfig)
    time.sleep(0.1)

    # Run experimentation
    networkParams = {"coarseGrainPositions": coarseGrainPositions, "fineGrainPositions": fineGrainPositions,
                     "offset": offset}
    global_events, global_timestamps = experimentation(board=board, numNeurons=numNeuronsEachPop,
                                                       rep=rep, wtimeDExperiment=wtimeDExperiment,
                                                       rtimeBExperiment=rtimeBExperiment,
                                                       wtimeBExperiments=wtimeBExperiments,
                                                       virtualPops=virtualPops, networkParams=networkParams)
    # Get visual data
    path, file = write_file(saveFigPath.replace(".png", ".txt"), "", "", {"global_events": global_events, "global_timestamps": global_timestamps})
    print(path)
    rasterplot_full_network_separate_inputs(global_events, global_timestamps, coarseGrainPositions, fineGrainPositions,
                            save=save, plot=plot, saveFigPath=saveFigPath)


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
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DENM_ETAU_P', 2, 40)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DENM_EGAIN_P', 4, 120)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DEGA_ITAU_P', 2, 40)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DEGA_IGAIN_P', 4, 40)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DESC_ITAU_P', 3, 40)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DESC_IGAIN_P', 0, 60)
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
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DENM_ETAU_P', 2, 40)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DENM_EGAIN_P', 4, 120)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DEGA_ITAU_P', 2, 5)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DEGA_IGAIN_P', 2, 47)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DESC_ITAU_P', 2, 40)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DESC_IGAIN_P', 0, 20)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYAM_W0_P', 5, 250)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYAM_W1_P', 5, 250)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYAM_W2_P', 5, 250)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYAM_W3_P', 5, 250)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYPD_EXT_N', 3, 200)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYPD_DLY0_P', 2, 200)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYPD_DLY1_P', 5, 200)
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
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DENM_ETAU_P', 2, 40)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DENM_EGAIN_P', 4, 150)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DEGA_ITAU_P', 2, 5)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DEGA_IGAIN_P', 2, 80)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DESC_ITAU_P', 2, 40)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'DESC_IGAIN_P', 0, 20)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYAM_W0_P', 5, 250)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYAM_W1_P', 5, 250)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYAM_W2_P', 5, 250)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYAM_W3_P', 5, 250)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYPD_EXT_N', 3, 200)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYPD_DLY0_P', 2, 200)
    set_parameter(myConfig.chips[chip].cores[core].parameters, 'SYPD_DLY1_P', 5, 200)
    # ** END CORE 3


def create_network(network, coarseGrainPositions, fineGrainPositions, numNeurons, chip, offset, fineGrainThreshold):
    # Create and connect virtual input and ring pop dummy (not working the first neuron/synapse)
    network.add_connection(source=network.add_virtual_group(size=1),
                           target=network.add_group(chip=0, core=0, size=1, name="dummy"),
                           probability=1, dendrite=Dendrite.ampa, weight=[False, False, False, False], repeat=16)
    # INPUT (VIRTUAL) POPULATION
    #   * inRobCP (input pop for coarse robot position)
    inRobCP_pops = [network.add_virtual_group(size=numNeurons) for _ in range(coarseGrainPositions)]
    #   * inRobFP (input pop for fine robot position)
    inRobFP_pops = [network.add_virtual_group(size=numNeurons) for _ in range(fineGrainPositions)]
    #   * inRefP (input pop for reference position)
    inRefP_pops = [network.add_virtual_group(size=numNeurons) for _ in range(coarseGrainPositions)]
    virtualPops = {"inRobCP_pops": inRobCP_pops, "inRobFP_pops": inRobFP_pops, "inRefP_pops": inRefP_pops}
    # END INPUT (VIRTUAL) POPULATION

    # WTA-SHIFTED
    print(" * Create WTA-shifted network")
    core = 0
    create_wta(network, chip, core, numNeurons, coarseGrainPositions, inRefP_pops, offset)
    # END WTA-SHIFTED

    # COMPARATOR
    print(" * Create comparator network")
    #   * Coarse grain comparator
    core = 2
    coarseOut_pops = create_coarse_comparator(network, chip, core, numNeurons, coarseGrainPositions, inRobCP_pops, inRefP_pops)
    #   * Fine grain comparator
    core = 1
    fineOut_pops = create_fine_comparator(network, chip, core, numNeurons, fineGrainThreshold, inRobFP_pops)
    #   * Coarse-Fine comparator
    core = 2
    create_out_comparator(network, chip, core, numNeurons, coarseOut_pops, fineOut_pops)
    # END COPARATOR

    # Dummy connections for fine grain positions not connected to anything
    for i in range(fineGrainPositions):
        if not(i == fineGrainThreshold):
            network.add_connection(source=inRobFP_pops[i],
                                   target=network.add_group(chip=0, core=0, size=1, name="dummy_robfp"),
                                   probability=1, dendrite=Dendrite.ampa, weight=[False, False, False, False],
                                   repeat=16)

    # Create all elements in board and check for problems
    print("* Deploy network")
    network.connect()
    # Debug information of the network
    print("(DEBUG) Virtual populations")
    for pop in network.virtual_groups:
        print("  " + str(pop.get_ids()) + " destinations=" + str(pop.get_destinations()))
    print("(DEBUG) Populations")
    for pop in network.groups:
        print("  " + str(pop.name) + " neurons=" + str(pop.neurons) + " ids=" + str(pop.ids) + " destinations=" + str(
            pop.destinations))
    print("(DEBUG) Synapses")
    for syn in network.connections:
        if type(syn.source) is VirtualGroup:
            print("  " + "Virtual-" + str(syn.target.name) + " (" + str(syn.dendrite) + ")")
        else:
            print("  " + str(syn.source.name) + "-" + str(syn.target.name) + " (" + str(syn.dendrite) + ")")
    return virtualPops


def create_wta(network, chip, core, numNeurons, numPop, inRefP_pops, offset):
    # Real populations (wta shifted pops)
    #   * outR (outer ring of wta shifted)
    outR_pops = [network.add_group(chip=chip, core=core, size=numNeurons, name="outR_" + str(i)) for i in range(numPop)]
    #   * inR (inner ring of wta shifted)
    inR_pops = [network.add_group(chip=chip, core=core, size=numNeurons, name="inR_" + str(i)) for i in range(numPop)]

    # Synapses
    for i in range(numPop):
        # inRefP_i - outR_i (exc)
        network.add_connection(source=inRefP_pops[i], target=outR_pops[i], probability=1, dendrite=Dendrite.ampa,
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


def create_coarse_comparator(network, chip, core, numNeurons, numPop, inRobP_pops, inRefP_pops):
    # Real populations (comparator units)
    #   * cmpRobP (robot position neuron in comparator)
    cmpRobP_pops = [network.add_group(chip=chip, core=core, size=numNeurons, name="cmp_c_robp_" + str(i)) for i in
                    range(numPop)]
    #   * cmpRefP (reference position neuron in comparator)
    cmpRefP_pops = [network.add_group(chip=chip, core=core, size=numNeurons, name="cmp_c_refp_" + str(i)) for i in
                    range(numPop)]
    #   * lInh (local inhibition neuron in comparator)
    lInh_pops = [network.add_group(chip=chip, core=core, size=numNeurons, name="cmp_c_linh_" + str(i)) for i in
                 range(numPop)]
    #   * cmpOut (output signal of comparator)
    cmpOut_pops = [network.add_group(chip=chip, core=core, size=numNeurons, name="cmp_c_out_" + str(i)) for i in
                   range(numPop)]

    # Synapses
    for i in range(numPop):
        # inRobP_i - cmpRobP_i (exc)
        network.add_connection(source=inRobP_pops[i], target=cmpRobP_pops[i], probability=1, dendrite=Dendrite.nmda,
                               weight=[True, True, True, True], repeat=16)
        # inRobP_i - lInh_i (exc)
        network.add_connection(source=inRobP_pops[i], target=lInh_pops[i], probability=1, dendrite=Dendrite.nmda,
                               weight=[True, True, True, True], repeat=16)
        # inRefP_i - cmpRefp_i (exc)
        network.add_connection(source=inRefP_pops[i], target=cmpRefP_pops[i], probability=1, dendrite=Dendrite.nmda,
                               weight=[True, True, True, True], repeat=16)
        # inRefP_i - lInh_i (exc)
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
    return cmpOut_pops


def create_fine_comparator(network, chip, core, numNeurons, fineGrainThreshold, inRobFP_pops):
    # Real populations (comparator units)
    cmpOut_pop = network.add_group(chip=chip, core=core, size=numNeurons, name="cmp_f_out_0")
    # Synapses
    network.add_connection(source=inRobFP_pops[fineGrainThreshold], target=cmpOut_pop, probability=1, dendrite=Dendrite.ampa,
                           weight=[True, True, True, True], repeat=16)
    return cmpOut_pop


def create_out_comparator(network, chip, core, numNeurons, coarseOut_pops, fineOut_pop):
    # Real populations (comparator units)
    #   * input A
    inA_pop = network.add_group(chip=chip, core=core, size=numNeurons, name="cmp_o_inA")
    #   * input B
    inB_pop = network.add_group(chip=chip, core=core, size=numNeurons, name="cmp_o_inB")
    #   * cmp A
    cmpA_pop = network.add_group(chip=chip, core=core, size=numNeurons, name="cmp_o_cmpA")
    #   * cmp B
    cmpB_pop = network.add_group(chip=chip, core=core, size=numNeurons, name="cmp_o_cmpB")
    #   * lInh (local inhibition neuron in comparator)
    lInh_pop = network.add_group(chip=chip, core=core, size=numNeurons, name="cmp_o_linh_0")
    #   * cmpOut (output signal of comparator)
    cmpOut_pop = network.add_group(chip=chip, core=core, size=numNeurons, name="signal_out")

    # Synapses
    #   * Input A
    for pop in coarseOut_pops:
        network.add_connection(source=pop, target=inA_pop, probability=1, dendrite=Dendrite.nmda,
                               weight=[True, True, True, True], repeat=16)
    #   * Input B
    network.add_connection(source=fineOut_pop, target=inB_pop, probability=1, dendrite=Dendrite.nmda,
                           weight=[True, True, True, True], repeat=16)

    #   * Normal cmp unit
    # inA - cmpA (exc)
    network.add_connection(source=inA_pop, target=cmpA_pop, probability=1, dendrite=Dendrite.nmda,
                           weight=[True, True, True, True], repeat=16)
    # inA - lInh_i (exc)
    network.add_connection(source=inA_pop, target=lInh_pop, probability=1, dendrite=Dendrite.ampa,
                           weight=[True, True, True, True], repeat=16)
    # inB - cmpB (exc)
    network.add_connection(source=inB_pop, target=cmpB_pop, probability=1, dendrite=Dendrite.nmda,
                           weight=[True, True, True, True], repeat=16)
    # inB - lInh_i (exc)
    network.add_connection(source=inB_pop, target=lInh_pop, probability=1, dendrite=Dendrite.ampa,
                           weight=[True, True, True, True], repeat=16)
    # cmpA - cmpOut (exc)
    network.add_connection(source=cmpA_pop, target=cmpOut_pop, probability=1, dendrite=Dendrite.nmda,
                           weight=[True, True, True, True], repeat=16)
    # cmpB - cmpOut (exc)
    network.add_connection(source=cmpB_pop, target=cmpOut_pop, probability=1, dendrite=Dendrite.nmda,
                           weight=[True, True, True, True], repeat=16)
    # lInh_i - cmpOut (inh)
    network.add_connection(source=lInh_pop, target=cmpOut_pop, probability=1, dendrite=Dendrite.gaba,
                           weight=[True, True, True, True], repeat=16, precise_delay=True, mismatched_delay=False)

    network.add_connection(source=lInh_pop, target=cmpOut_pop, probability=1, dendrite=Dendrite.shunt,
                           weight=[True, False, False, False], repeat=16)


def experimentation(board, numNeurons, rep, wtimeDExperiment, rtimeBExperiment, wtimeBExperiments, virtualPops, networkParams):
    global_events = []
    global_timestamps = []
    t_global = 0
    inRobCP_pops = virtualPops["inRobCP_pops"]
    inRobFP_pops = virtualPops["inRobFP_pops"]
    inRefP_pops = virtualPops["inRefP_pops"]
    offset = networkParams["offset"]
    coarseGrainPositions = networkParams["coarseGrainPositions"]
    fineGrainPositions = networkParams["fineGrainPositions"]
    signalNeuron = fineGrainPositions + coarseGrainPositions*9 + 4
    print("Signal neuron = " + str(signalNeuron))

    # Ascending trayectory: from 0 to N-1-offset
    refPositions = [i for i in range(coarseGrainPositions-1)]
    robFPositions = [i for i in range(fineGrainPositions)]
    robCPositions = [i for i in range(coarseGrainPositions)]

    out_signal_activate = True
    refIndex = 0
    ref_pos_events = []
    print("")
    for robCPos in robCPositions:
        # Rob coarse pos events
        neurons = [i for i in range(numNeurons) for _ in range(rep)]
        timestamps = [r + i * wtimeDExperiment for i in range(numNeurons) for r in range(rep)]
        rob_c_pos_events = isi_gen(virtual_group=inRobCP_pops[robCPos], neurons=neurons, timestamps=timestamps)
        print("(DEBUG) Input robP events")
        print("    (id, tag, chip/core, t)")
        print("    " + str(rob_c_pos_events))

        for robFPos in robFPositions:
            if out_signal_activate and not(refIndex == len(refPositions)):
                # Ref pos events
                refPos = refPositions[refIndex]
                neurons = [i for i in range(numNeurons) for _ in range(rep)]
                timestamps = [r + i * wtimeDExperiment for i in range(numNeurons) for r in range(rep)]
                ref_pos_events = isi_gen(virtual_group=inRefP_pops[refPos], neurons=neurons, timestamps=timestamps)
                print("(DEBUG) Input refP events")
                print("    (id, tag, chip/core, t)")
                print("    " + str(ref_pos_events))
                out_signal_activate = False
                refIndex = refIndex+1
            # Rob fine pos events
            neurons = [i for i in range(numNeurons) for _ in range(rep)]
            timestamps = [r + i * wtimeDExperiment for i in range(numNeurons) for r in range(rep)]
            rob_f_pos_events = isi_gen(virtual_group=inRobFP_pops[robFPos], neurons=neurons, timestamps=timestamps)
            print("(DEBUG) Input robP events")
            print("    (id, tag, chip/core, t)")
            print("    " + str(rob_f_pos_events))
            input_events = ref_pos_events + rob_c_pos_events + rob_f_pos_events

            print("\n\n\n***** Reference position " + str(refPos) + " *****")
            print("\n  *** Coarse robot position " + str(robCPos) + " ***  ")
            print("\n  *** Fine robot position " + str(robFPos) + " ***  ")

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

            if signalNeuron in output_events[0]:
                out_signal_activate = True
            t_global = timestamp_formated[len(timestamp_formated) - 1] + wtimeBExperiments
            global_events.append(output_events[0])
            global_timestamps.append(timestamp_formated)
    return global_events, global_timestamps