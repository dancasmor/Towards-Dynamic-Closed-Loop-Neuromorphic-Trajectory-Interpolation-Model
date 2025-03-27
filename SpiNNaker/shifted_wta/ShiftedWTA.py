import os
import json


class ShiftedWTA:

    def __init__(self, numPositions, offset, sim, configFilePath=False):
        self.numPositions = numPositions
        self.offset = offset
        self.sim = sim
        if configFilePath:
            self.configFilePath = configFilePath
        else:
            self.configFilePath = os.path.dirname(__file__) + "/swta_config.json"

        # Create the synapse mapping between OutRing and InnerRing of WTA with shifted connections
        self.create_synapse_mapping()
        # Load network config parameters
        self.load_config_files()
        # Create populations and memories
        self.create_populations()
        # Create synapses
        self.create_synapses()

    def create_synapse_mapping(self):
        synapseMap = []
        for i in range(self.numPositions):
            synapseMap.append((i, (i + self.offset) % self.numPositions))
        self.synapseMap = synapseMap

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
        # Create OutRingLayer population
        self.OutRingLayer = self.sim.Population(self.numPositions, self.sim.IF_curr_exp(**self.neuronParameters["OutRingLayer"]), label="OutRingLayer")
        self.OutRingLayer.set(v=self.initNeuronParameters["OutRingLayer"]["vInit"])
        # Create InnerRingLayer population
        self.InnerRingLayer = self.sim.Population(self.numPositions, self.sim.IF_curr_exp(**self.neuronParameters["InnerRingLayer"]), label="InnerRingLayer")
        self.InnerRingLayer.set(v=self.initNeuronParameters["InnerRingLayer"]["vInit"])

    def create_synapses(self):
        # + OutRingLayer-InnerRingLayer
        self.OutRingLayer_InnerRingLayer = self.sim.Projection(self.OutRingLayer,
                                                      self.InnerRingLayer,
                                                      self.sim.FromListConnector(self.synapseMap),
                                                      synapse_type=self.sim.StaticSynapse(
                                                          weight=self.synParameters["OutRingLayer-InnerRingLayer"]["initWeight"],
                                                                    delay=self.synParameters["OutRingLayer-InnerRingLayer"]["delay"]),
                                                      receptor_type= self.synParameters["OutRingLayer-InnerRingLayer"]["receptor_type"]
                                                      )
        # + InnerRingLayer-InnerRingLayer
        self.InnerRingLayer_InnerRingLayer = self.sim.Projection(self.InnerRingLayer,
                                                      self.InnerRingLayer,
                                                      self.sim.AllToAllConnector(allow_self_connections=False),
                                                      synapse_type=self.sim.StaticSynapse(
                                                          weight=self.synParameters["InnerRingLayer-InnerRingLayer"]["initWeight"],
                                                          delay=self.synParameters["InnerRingLayer-InnerRingLayer"]["delay"]),
                                                      receptor_type=self.synParameters["InnerRingLayer-InnerRingLayer"]["receptor_type"]
                                                      )


    def connect_input(self, InputLayer, customInSynParameters=False):
        if customInSynParameters:
            self.customInSynParameters = customInSynParameters
        else:
            self.customInSynParameters = self.synParameters
        # + InputLayer-OutRingLayer
        self.InputLayer_OutRingLayer = self.sim.Projection(InputLayer,
                                                      self.OutRingLayer,
                                                      self.sim.OneToOneConnector(),
                                                      synapse_type=self.sim.StaticSynapse(
                                                          weight=self.customInSynParameters["InputLayer-OutRingLayer"]["initWeight"],
                                                          delay=self.customInSynParameters["InputLayer-OutRingLayer"]["delay"]),
                                                      receptor_type=self.customInSynParameters["InputLayer-OutRingLayer"][
                                                          "receptor_type"]
                                                      )

    def connect_output(self, SWTAOutLayer, customOutSynParameters=False):
        if customOutSynParameters:
            self.customOutSynParameters = customOutSynParameters
        else:
            self.customOutSynParameters = self.synParameters
        # + InnerRingLayer-SWTAOutLayer
        self.InnerRingLayer_SWTAOutLayer = self.sim.Projection(self.InnerRingLayer,
                                                            SWTAOutLayer,
                                                            self.sim.OneToOneConnector(),
                                                            synapse_type=self.sim.StaticSynapse(
                                                                weight=self.customOutSynParameters["InnerRingLayer-SWTAOutLayer"]["initWeight"],
                                                                delay=self.customOutSynParameters["InnerRingLayer-SWTAOutLayer"]["delay"]),
                                                            receptor_type=self.customOutSynParameters["InnerRingLayer-SWTAOutLayer"]["receptor_type"]
                                                            )