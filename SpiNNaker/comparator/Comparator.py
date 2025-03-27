import os
import json


class Comparator:

    def __init__(self, numPositions, sim, configFilePath=False):
        self.numPositions = numPositions
        self.sim = sim
        if configFilePath:
            self.configFilePath = configFilePath
        else:
            self.configFilePath = os.path.dirname(__file__) + "/comparator_config.json"

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
        # Create RobPLayer population
        self.RobPLayer = self.sim.Population(self.numPositions, self.sim.IF_curr_exp(**self.neuronParameters["RobPLayer"]), label="RobPLayer")
        self.RobPLayer.set(v=self.initNeuronParameters["RobPLayer"]["vInit"])
        # Create RefPLayer population
        self.RefPLayer = self.sim.Population(self.numPositions, self.sim.IF_curr_exp(**self.neuronParameters["RefPLayer"]), label="RefPLayer")
        self.RefPLayer.set(v=self.initNeuronParameters["RefPLayer"]["vInit"])
        # Create InhLayer population
        self.InhLayer = self.sim.Population(self.numPositions, self.sim.IF_curr_exp(**self.neuronParameters["InhLayer"]), label="InhLayer")
        self.InhLayer.set(v=self.initNeuronParameters["InhLayer"]["vInit"])
        # Create CmpOutLayer population
        self.CmpOutLayer = self.sim.Population(self.numPositions, self.sim.IF_curr_exp(**self.neuronParameters["CmpOutLayer"]), label="CmpOutLayer")
        self.CmpOutLayer.set(v=self.initNeuronParameters["CmpOutLayer"]["vInit"])

    def create_synapses(self):
        # + RobPLayer-CmpOutLayer
        self.RobPLayer_CmpOutLayer = self.sim.Projection(self.RobPLayer,
                                                      self.CmpOutLayer,
                                                      self.sim.OneToOneConnector(),
                                                      synapse_type=self.sim.StaticSynapse(
                                                          weight=self.synParameters["RobPLayer-CmpOutLayer"]["initWeight"],
                                                                    delay=self.synParameters["RobPLayer-CmpOutLayer"]["delay"]),
                                                      receptor_type= self.synParameters["RobPLayer-CmpOutLayer"]["receptor_type"]
                                                      )
        # + RefPLayer-CmpOutLayer
        self.RefPLayer_CmpOutLayer = self.sim.Projection(self.RefPLayer,
                                                      self.CmpOutLayer,
                                                      self.sim.OneToOneConnector(),
                                                      synapse_type=self.sim.StaticSynapse(
                                                          weight=self.synParameters["RefPLayer-CmpOutLayer"]["initWeight"],
                                                          delay=self.synParameters["RefPLayer-CmpOutLayer"]["delay"]),
                                                      receptor_type=self.synParameters["RefPLayer-CmpOutLayer"]["receptor_type"]
                                                      )
        # + InhLayer-CmpOutLayer
        self.InhLayer_CmpOutLayer = self.sim.Projection(self.InhLayer,
                                                      self.CmpOutLayer,
                                                      self.sim.OneToOneConnector(),
                                                      synapse_type=self.sim.StaticSynapse(
                                                          weight=self.synParameters["InhLayer-CmpOutLayer"]["initWeight"],
                                                          delay=self.synParameters["InhLayer-CmpOutLayer"]["delay"]),
                                                      receptor_type=self.synParameters["InhLayer-CmpOutLayer"]["receptor_type"]
                                                      )

    def connect_input(self, RobPInputLayer, RefPInputLayer, customInSynParameters=False, allConnection=False):
        if customInSynParameters:
            self.customInSynParameters = customInSynParameters
        else:
            self.customInSynParameters = self.synParameters

        if not allConnection:
            # + RobPInputLayer-RobPLayer
            self.RobPInputLayer_RobPLayer = self.sim.Projection(RobPInputLayer,
                                                          self.RobPLayer,
                                                          self.sim.OneToOneConnector(),
                                                          synapse_type=self.sim.StaticSynapse(
                                                              weight=self.customInSynParameters["RobPInputLayer-RobPLayer"]["initWeight"],
                                                              delay=self.customInSynParameters["RobPInputLayer-RobPLayer"]["delay"]),
                                                          receptor_type=self.customInSynParameters["RobPInputLayer-RobPLayer"][
                                                              "receptor_type"]
                                                          )
            # + RefPInputLayer-RefPLayer
            self.RefPInputLayer_RefPLayer = self.sim.Projection(RefPInputLayer,
                                                          self.RefPLayer,
                                                          self.sim.OneToOneConnector(),
                                                          synapse_type=self.sim.StaticSynapse(
                                                              weight=self.customInSynParameters["RefPInputLayer-RefPLayer"]["initWeight"],
                                                              delay=self.customInSynParameters["RefPInputLayer-RefPLayer"]["delay"]),
                                                          receptor_type=self.customInSynParameters["RefPInputLayer-RefPLayer"][
                                                              "receptor_type"]
                                                          )
            # + RobPInputLayer-InhLayer
            self.RobPInputLayer_RobPLayer = self.sim.Projection(RobPInputLayer,
                                                                self.InhLayer,
                                                                self.sim.OneToOneConnector(),
                                                                synapse_type=self.sim.StaticSynapse(
                                                                    weight=self.customInSynParameters["RobPInputLayer-InhLayer"]["initWeight"],
                                                                    delay=self.customInSynParameters["RobPInputLayer-InhLayer"]["delay"]),
                                                                receptor_type=self.customInSynParameters["RobPInputLayer-InhLayer"]["receptor_type"]
                                                                )
            # + RefPInputLayer-InhLayer
            self.RefPInputLayer_RefPLayer = self.sim.Projection(RefPInputLayer,
                                                                self.InhLayer,
                                                                self.sim.OneToOneConnector(),
                                                                synapse_type=self.sim.StaticSynapse(
                                                                    weight=self.customInSynParameters["RefPInputLayer-InhLayer"]["initWeight"],
                                                                    delay=self.customInSynParameters["RefPInputLayer-InhLayer"]["delay"]),
                                                                receptor_type=self.customInSynParameters["RefPInputLayer-InhLayer"]["receptor_type"]
                                                                )
        else:
            # + RobPInputLayer-RobPLayer
            self.RobPInputLayer_RobPLayer = self.sim.Projection(RobPInputLayer,
                                                                self.RobPLayer,
                                                                self.sim.AllToAllConnector(allow_self_connections=True),
                                                                synapse_type=self.sim.StaticSynapse(
                                                                    weight=self.customInSynParameters[
                                                                        "RobPInputLayer-RobPLayer"]["initWeight"],
                                                                    delay=self.customInSynParameters[
                                                                        "RobPInputLayer-RobPLayer"]["delay"]),
                                                                receptor_type=
                                                                self.customInSynParameters["RobPInputLayer-RobPLayer"][
                                                                    "receptor_type"]
                                                                )
            # + RefPInputLayer-RefPLayer
            self.RefPInputLayer_RefPLayer = self.sim.Projection(RefPInputLayer,
                                                                self.RefPLayer,
                                                                self.sim.AllToAllConnector(allow_self_connections=True),
                                                                synapse_type=self.sim.StaticSynapse(
                                                                    weight=self.customInSynParameters[
                                                                        "RefPInputLayer-RefPLayer"]["initWeight"],
                                                                    delay=self.customInSynParameters[
                                                                        "RefPInputLayer-RefPLayer"]["delay"]),
                                                                receptor_type=
                                                                self.customInSynParameters["RefPInputLayer-RefPLayer"][
                                                                    "receptor_type"]
                                                                )
            # + RobPInputLayer-InhLayer
            self.RobPInputLayer_RobPLayer = self.sim.Projection(RobPInputLayer,
                                                                self.InhLayer,
                                                                self.sim.AllToAllConnector(allow_self_connections=True),
                                                                synapse_type=self.sim.StaticSynapse(
                                                                    weight=self.customInSynParameters[
                                                                        "RobPInputLayer-InhLayer"]["initWeight"],
                                                                    delay=self.customInSynParameters[
                                                                        "RobPInputLayer-InhLayer"]["delay"]),
                                                                receptor_type=
                                                                self.customInSynParameters["RobPInputLayer-InhLayer"][
                                                                    "receptor_type"]
                                                                )
            # + RefPInputLayer-InhLayer
            self.RefPInputLayer_RefPLayer = self.sim.Projection(RefPInputLayer,
                                                                self.InhLayer,
                                                                self.sim.AllToAllConnector(allow_self_connections=True),
                                                                synapse_type=self.sim.StaticSynapse(
                                                                    weight=self.customInSynParameters[
                                                                        "RefPInputLayer-InhLayer"]["initWeight"],
                                                                    delay=self.customInSynParameters[
                                                                        "RefPInputLayer-InhLayer"]["delay"]),
                                                                receptor_type=
                                                                self.customInSynParameters["RefPInputLayer-InhLayer"][
                                                                    "receptor_type"]
                                                                )


    def connect_output(self, ComparatorOutLayer, customOutSynParameters=False):
        if customOutSynParameters:
            self.customOutSynParameters = customOutSynParameters
        else:
            self.customOutSynParameters = self.synParameters
        # + CmpOutLayer-ComparatorOutLayer
        self.CmpOutLayer_ComparatorOutLayer = self.sim.Projection(self.CmpOutLayer,
                                                            ComparatorOutLayer,
                                                            self.sim.OneToOneConnector(),
                                                            synapse_type=self.sim.StaticSynapse(
                                                                weight=self.customOutSynParameters["CmpOutLayer-ComparatorOutLayer"]["initWeight"],
                                                                delay=self.customOutSynParameters["CmpOutLayer-ComparatorOutLayer"]["delay"]),
                                                            receptor_type=self.customOutSynParameters["CmpOutLayer-ComparatorOutLayer"]["receptor_type"]
                                                            )