import os
import json
from shifted_wta.ShiftedWTA import ShiftedWTA
from comparator.Comparator import Comparator


class SpikingInterpolator:

    def __init__(self, coarsePositions, finePositions, offset, sim, configFilePath=False):
        self.coarsePositions = coarsePositions
        self.finePositions = finePositions
        self.offset = offset
        self.sim = sim
        if configFilePath:
            self.configFilePath = configFilePath
        else:
            self.configFilePath = os.path.dirname(__file__) + "/spiking_interpolator_config.json"

        # Load network config parameters
        self.load_config_files()
        # Create populations and memories
        self.create_populations()
        # Create synapses
        self.create_synapses()

    def load_config_files(self):
        # Read config file
        try:
            file = open(self.configFilePath)
            network_config = json.load(file)
        except FileNotFoundError:
            raise Exception("Network config file not found in " + self.configFilePath)
        # + Neurons paramaters
        self.neuronParameters = network_config["neuronParameters"]
        # + Initial neuron parameters
        self.initNeuronParameters = network_config["initNeuronParameters"]
        # + Synapses parameters
        self.synParameters = network_config["synParameters"]

    def create_populations(self):
        # Create SWTA
        self.SWTA = ShiftedWTA(self.coarsePositions, self.offset, self.sim)
        # Create comparator coarse grain
        self.CoarseGrainComparator = Comparator(self.coarsePositions, self.sim)
        # Create comparator fine grain
        #self.FineGrainComparator = Comparator(self.finePositions, self.sim)
        self.FineGrainComparator = self.sim.Population(1,
                                                       self.sim.IF_curr_exp(**self.neuronParameters["FineGrainComparator"]),
                                                       label="FineGrainComparator")

        self.FineGrainComparator.set(v=self.initNeuronParameters["FineGrainComparator"]["vInit"])
        # Create comparator output
        self.OutputComparator = Comparator(1, self.sim)


    def create_synapses(self):
        # + CoarseGrainComparator-OutputComparator
        # + FineGrainComparator-OutputComparator
        self.OutputComparator.connect_input(self.CoarseGrainComparator.CmpOutLayer, self.FineGrainComparator, allConnection=True)

    def connect_input(self, RobCoarsePInputLayer, RobFinePInputLayer, RefPInputLayer, customInSynParameters=False):
        if customInSynParameters:
            self.customInSynParameters = customInSynParameters
        else:
            self.customInSynParameters = self.synParameters

        # + RobCoarsePInputLayer-CoarseGrainComparator
        # + RefPInputLayer-CoarseGrainComparator
        self.CoarseGrainComparator.connect_input(RobCoarsePInputLayer, RefPInputLayer)

        # + RobFinePInputLayer-FineGrainComparator
        self.RobFinePInputLayer_FineGrainComparator = self.sim.Projection(self.sim.PopulationView(RobFinePInputLayer, [1]),
                                                      self.FineGrainComparator,
                                                      self.sim.OneToOneConnector(),
                                                      synapse_type=self.sim.StaticSynapse(
                                                          weight=self.customInSynParameters["RefPInputLayer-FineGrainComparator"]["initWeight"],
                                                          delay=self.customInSynParameters["RefPInputLayer-FineGrainComparator"]["delay"]),
                                                      receptor_type=self.customInSynParameters["RefPInputLayer-FineGrainComparator"]["receptor_type"]
                                                      )
        # + RefPInputLayer-SWTA
        self.SWTA.connect_input(RefPInputLayer)

    def connect_output(self, OutputSWTALayer, OutputCmpLayer, customOutSynParameters=False):
        if customOutSynParameters:
            self.customOutSynParameters = customOutSynParameters
        else:
            self.customOutSynParameters = self.synParameters
        # + SWTA-OutputSWTALayer
        self.SWTA.connect_output(OutputSWTALayer)
        # + OutputComparator-OutputCmpLayer
        self.OutputComparator.connect_output(OutputCmpLayer)