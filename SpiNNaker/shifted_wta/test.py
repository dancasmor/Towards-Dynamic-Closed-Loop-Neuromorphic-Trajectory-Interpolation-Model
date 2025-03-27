
import sys
sys.path.append('..')
import plot
from ShiftedWTA import ShiftedWTA
import spynnaker8 as sim

def main():
    # Parameters
    numPositions = 4
    offset = 1
    #inputSpikes = [[0], [5], [10], [15]]
    inputSpikes = [[0,1,2,3,4,5], [10,11,12,13,14,15], [20,21,22,23,24,25], [30,31,32,33,34,35]]
    #simTime = 20
    simTime = 40
    saveFigPath = "resultsExp0.png"

    # * Setup simulation
    timestep = 1.0
    sim.setup(timestep)

    # * Create network
    #       - Create SWTA
    wta = ShiftedWTA(numPositions, offset, sim)
    #       - Create input and output populations
    #       - Input layer: spikes generators
    InputLayer = sim.Population(numPositions, sim.SpikeSourceArray(spike_times=inputSpikes),
                                         label="InputLayer")
    #       - Output layer: fire a spike when receive a spike
    neuronParameters = {"cm": 0.27, "i_offset": 0.0, "tau_m": 3.0, "tau_refrac": 1.0, "tau_syn_E": 0.3,
                        "tau_syn_I": 0.3, "v_reset": -60.0, "v_rest": -60.0, "v_thresh": -57.0}
    OutputLayer = sim.Population(1, sim.IF_curr_exp(**neuronParameters), label="OutputLayer")
    OutputLayer.set(v=-60)
    #       - Input and Output to SWTA
    wta.connect_input(InputLayer)
    wta.connect_output(OutputLayer)

    # * Set populations to record spikes
    wta.OutRingLayer.record(["spikes"])
    wta.InnerRingLayer.record(["spikes"])
    #OutputLayer.record(["spikes"])

    # * Run simulation
    sim.run(simTime)

    # * Get spike information
    formatSpikes = get_spikes_information(inputSpikes, wta, OutputLayer)

    # * End simulation
    sim.end()

    # * Generate plot
    plot.rasterplot(formatSpikes, saveFigPath=saveFigPath)

    print("Finished!")


def get_spikes_information(inputSpikes, wta, outputLayer):
    formatSpikes = {}
    formatSpikes["inputSpikes"] = inputSpikes
    populations = {
        "OutRingLayer": wta.OutRingLayer,
        "InnerRingLayer": wta.InnerRingLayer#, "OutputLayer": outputLayer
    }
    for key, value in populations.items():
        spikes = value.get_data(variables=["spikes"]).segments[0].spiketrains
        formatSpikes[key] = []
        for neuron in spikes:
            formatSpikes[key].append(neuron.as_array().tolist())
    # Add spike information to class variable
    return formatSpikes

if __name__ == "__main__":
    main()