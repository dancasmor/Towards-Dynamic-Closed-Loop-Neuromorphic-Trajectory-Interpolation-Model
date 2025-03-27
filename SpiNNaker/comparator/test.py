
import sys
sys.path.append('..')
import plot
from Comparator import Comparator
import spynnaker8 as sim

def main():
    # Parameters
    numPositions = 4
    inputRobSpikes = [[30, 35, 40, 45], [55, 60, 65, 70], [80, 85, 90, 95], [105, 110, 115, 120]]
    inputRefSpikes = [[5, 30, 55, 80, 105], [10, 35, 60, 85, 110], [15, 40, 65, 90, 115], [20, 45, 70, 95, 120]]
    timeExpLimit = [0, 25, 50, 75, 100, 125]
    simTime = 125
    saveFigPath = "resultsExp0.png"

    # * Setup simulation
    timestep = 1.0
    sim.setup(timestep)

    # * Create network
    #       - Create Comparator
    comparator = Comparator(numPositions, sim)
    #       - Create input and output populations
    #       - Input layer: spikes generators
    InputRobLayer = sim.Population(numPositions, sim.SpikeSourceArray(spike_times=inputRobSpikes), label="InputRobLayer")
    InputRefLayer = sim.Population(numPositions, sim.SpikeSourceArray(spike_times=inputRefSpikes), label="InputRefLayer")
    #       - Output layer: fire a spike when receive a spike
    neuronParameters = {"cm": 0.27, "i_offset": 0.0, "tau_m": 3.0, "tau_refrac": 1.0, "tau_syn_E": 0.3,
                        "tau_syn_I": 0.3, "v_reset": -60.0, "v_rest": -60.0, "v_thresh": -57.0}
    OutputLayer = sim.Population(numPositions, sim.IF_curr_exp(**neuronParameters), label="OutputLayer")
    OutputLayer.set(v=-60)
    #       - Input and Output to Comparator
    comparator.connect_input(InputRobLayer, InputRefLayer)
    comparator.connect_output(OutputLayer)

    # * Set populations to record spikes
    comparator.RobPLayer.record(["spikes"])
    comparator.RefPLayer.record(["spikes"])
    comparator.InhLayer.record(["spikes"])
    comparator.CmpOutLayer.record(["spikes"])

    # * Run simulation
    sim.run(simTime)

    # * Get spike information
    formatSpikes = get_spikes_information(inputRobSpikes, inputRefSpikes, comparator, OutputLayer)

    # * End simulation
    sim.end()

    # * Generate plot
    plot.rasterplot_comparator(formatSpikes, numPositions, timeExpLimit, saveFigPath=saveFigPath)

    print("Finished!")


def get_spikes_information(inputRobSpikes, inputRefSpikes, comparator, outputLayer):
    formatSpikes = {}
    formatSpikes["inputRobSpikes"] = inputRobSpikes
    formatSpikes["inputRefSpikes"] = inputRefSpikes
    populations = {
        "RobPLayer": comparator.RobPLayer,
        "RefPLayer": comparator.RefPLayer,
        "InhLayer": comparator.InhLayer,
        "CmpOutLayer": comparator.CmpOutLayer#, "OutputLayer": outputLayer
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