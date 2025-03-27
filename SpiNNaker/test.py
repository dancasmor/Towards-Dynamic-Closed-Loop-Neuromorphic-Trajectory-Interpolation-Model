import plot
from SpikingInterpolator import SpikingInterpolator
import spynnaker8 as sim

def main():
    # Parameters
    numPositions = 4
    offset = 1
    inputRobCoarseSpikes = [[5, 10, 15, 20], [25, 30, 35, 40], [45, 50, 55, 60], [65, 70, 75, 80]]
    inputRobFineSpikes = [[6, 26, 46, 66], [11, 31, 51, 71], [16, 36, 56, 76], [21, 41, 61, 81]]
    inputRefSpikes = [[5, 10], [15, 20, 25, 30], [35, 40, 45, 50], [55, 60, 65, 70, 75, 80]]
    simTime = 90
    saveFigPath = "resultsExp0.png"

    # * Setup simulation
    timestep = 1.0
    sim.setup(timestep)

    # * Create network
    #       - Create SpikingInterpolator
    interpolator = SpikingInterpolator(numPositions, numPositions, offset, sim)
    #       - Input layer: spikes generators
    InputRobCoarseLayer = sim.Population(numPositions, sim.SpikeSourceArray(spike_times=inputRobCoarseSpikes), label="InputRobCoarseLayer")
    InputRobFineLayer = sim.Population(numPositions, sim.SpikeSourceArray(spike_times=inputRobFineSpikes), label="InputRobFineLayer")
    InputRefLayer = sim.Population(numPositions, sim.SpikeSourceArray(spike_times=inputRefSpikes), label="InputRefLayer")
    #       - Connect input
    interpolator.connect_input(InputRobCoarseLayer, InputRobFineLayer, InputRefLayer)

    # * Set populations to record spikes
    interpolator.SWTA.OutRingLayer.record(["spikes"])
    interpolator.SWTA.InnerRingLayer.record(["spikes"])
    interpolator.CoarseGrainComparator.RobPLayer.record(["spikes"])
    interpolator.CoarseGrainComparator.RefPLayer.record(["spikes"])
    interpolator.CoarseGrainComparator.InhLayer.record(["spikes"])
    interpolator.CoarseGrainComparator.CmpOutLayer.record(["spikes"])
    interpolator.FineGrainComparator.record(["spikes"])
    interpolator.OutputComparator.RobPLayer.record(["spikes"])
    interpolator.OutputComparator.RefPLayer.record(["spikes"])
    interpolator.OutputComparator.InhLayer.record(["spikes"])
    interpolator.OutputComparator.CmpOutLayer.record(["spikes"])

    # * Run simulation
    sim.run(simTime)

    # * Get spike information
    formatSpikes = get_spikes_information(inputRobCoarseSpikes, inputRobFineSpikes, inputRefSpikes, interpolator)

    # * End simulation
    sim.end()

    # * Generate plot
    plot.rasterplot_full_network_separate_inputs(formatSpikes, numPositions, numPositions, saveFigPath=saveFigPath)

    print("Finished!")


def get_spikes_information(inputRobCoarseSpikes, inputRobFineSpikes, inputRefSpikes, interpolator):
    formatSpikes = {}
    formatSpikes["inputRobCoarseSpikes"] = inputRobCoarseSpikes
    formatSpikes["inputRobFineSpikes"] = inputRobFineSpikes
    formatSpikes["inputRefSpikes"] = inputRefSpikes
    populations = {
        "WTAOutRingLayer": interpolator.SWTA.OutRingLayer,
        "WTAInnerRingLayer": interpolator.SWTA.InnerRingLayer,
        "CGRobPLayer": interpolator.CoarseGrainComparator.RobPLayer,
        "CGRefPLayer": interpolator.CoarseGrainComparator.RefPLayer,
        "CGInhLayer": interpolator.CoarseGrainComparator.InhLayer,
        "CGCmpOutLayer": interpolator.CoarseGrainComparator.CmpOutLayer,
        "FGcmp": interpolator.FineGrainComparator,
        "OGRobPLayer": interpolator.OutputComparator.RobPLayer,
        "OGRefPLayer": interpolator.OutputComparator.RefPLayer,
        "OGInhLayer": interpolator.OutputComparator.InhLayer,
        "OGCmpOutLayer": interpolator.OutputComparator.CmpOutLayer
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