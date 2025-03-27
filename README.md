# Towards a Dynamic Closed-Loop Neuromorphic Trajectory Interpolation Model: Hardware Emulation and Software Simulation

<h2 name="Description">Description</h2>
<p align="justify">
Code on which the paper entitled "Towards a Dynamic Closed-Loop Neuromorphic Trajectory Interpolation Model: Hardware Emulation and Software Simulation" is based, sent to a journal and awaiting review.
</p>
<p align="justify">
This is a first approach to a closed-loop dynamic trajectory interpolation neuromorphic model for the control of robotic arm trajectories. This model has been implemented using Spiking Neural Networks (SNN) on two neuromorphic hardware platforms: <a href="https://www.synsense.ai/products/neuromorphic-chip-dynap-se2/">DYNAP-SE2</a> and <a href="https://apt.cs.manchester.ac.uk/projects/SpiNNaker/">SpiNNaker</a>. DYNAP-SE2 offers an analog hardware emulation of the model, compared to the digital software simulation of SpiNNaker. The code for the implementations is developed in Python using the <a href="https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjaxOCWhrn3AhVL1BoKHVtQDvsQFnoECAkQAQ&url=https%3A%2F%2Fgithub.com%2FSpiNNakerManchester%2FsPyNNaker&usg=AOvVaw3e3TBMJ-08yBqtsKza_RiE">sPyNNaker</a> libraries for SpiNNaker and <a href="https://www.synsense.ai/products/samna/">Samna</a> for DYNAP-SE2.
</p>
<p align="justify">
Please go to section <a href="#CiteThisWork">cite this work</a> to learn how to properly reference this work.
</p>


<h2>Table of contents</h2>
<p align="justify">
<ul>
<li><a href="#Description">Description</a></li>
<li><a href="#Article">Article</a></li>
<li><a href="#Instalation">Instalation</a></li>
<li><a href="#Usage">Usage</a></li>
<li><a href="#RepositoryContent">Repository content</a></li>
<li><a href="#CiteThisWork">Cite this work</a></li>
<li><a href="#Credits">Credits</a></li>
<li><a href="#License">License</a></li>
</ul>
</p>


<h2 name="Article">Article</h2>
<p align="justify">
<strong>Title</strong>: Towards a Dynamic Closed-Loop Neuromorphic Trajectory Interpolation Model: Hardware Emulation and Software Simulation

<strong>Abstract</strong>: Neuromorphic engineering aims to incorporate the computational principles found in animal brains, into modern technological systems. Following this approach, in this study we present a closed-loop neuromorphic control system for event-based robotic arms, highlighting a dynamic approach to trajectory interpolation through hardware emulation and software simulation. Our model employs a Shifted Winner-Take-All spiking network to interpolate reference trajectories and a spiking comparator network to ensure trajectory continuity against real-time positions, closing the control loop dynamically. Implementing the model on various neuromorphic platforms highlights its flexibility and adaptability across distinct computational paradigms, such as analog hardware emulation and digital software simulation. Experimental evaluations reveal robust, energy-efficient performance from the analog implementation and precise, stable operations from the digital paradigm. These results affirm the model's potential for enhanced robotic trajectory control and pave the way for future neuromorphic robotic control systems.

<strong>Keywords</strong>: Trajectory interpolation, Spiking Neural Networks, DYNAP-SE2, SpiNNaker, neuromorphic control

<strong>Corresponding Author</strong>: Daniel Casanueva-Morato

<strong>Contact</strong>: dcasanueva@us.es
</p>


<h2 name="Instalation">Instalation</h2>
<p align="justify">
<ol>
	<li>Have or have access to the SpiNNaker and DYNAP-SE2 hardware platform</li>
	<li>Python version 3.8.10</li>
	<li>Python libraries:</li>
	<ul>
		<li><p align="justify"><strong>sPyNNaker8</strong> or sPyNNaker (changing "import spynnaker8 as sim" to import "pyNN.spiNNaker as sim")</p></li>
		<li><strong>samna</strong> 0.9.24.0</li>
		<li><strong>matplotlib</strong> 3.5.2</li>
		<li><strong>numpy</strong> 1.22.4</li>
	</ul>
</ol>
</p>
<p align="justify">
To run any script, follow the python nomenclature: <code>python script.py</code>
</p>


<h2 name="RepositoryContent">Repository content</h3>
<p align="justify">
<ul>
	<li><p align="justify"><a href="DYNAP-SE2/">DYNAP-SE2</a> folder: DYNAP-SE2 implementation of the dynamic interpolation model.</p></li>
		<ul>
			<li><p align="justify"><a href="DYNAP-SE2/main.py">main.py</a>: script where the configuration and communication with the board to be used and the experiment to be performed are defined.</p></li>
			<li><p align="justify"><a href="DYNAP-SE2/plots/">plots</a> folder: contains all the plots generated and used in the paper.</p></li>
			<li><p align="justify"><a href="DYNAP-SE2/lib/">lib</a> folder: local utility library to facilitate the construction of SNN on DYNAP-SE2 using samna (available upon request).</p></li>
			<li><p align="justify"><a href="DYNAP-SE2/robot_control/">robot_control</a> folder: contains the declaration and experimentation of the different networks used to implement the model: <a href="DYNAP-SE2/robot_control/comparator.py">comparator</a>, <a href="DYNAP-SE2/robot_control/wta_shifted_4joints.py">WTA</a> and <a href="DYNAP-SE2/robot_control/robot_control_separate_inputs.py">complete system</a>.</p></li>
		</ul>
	<li><p align="justify"><a href="SpiNNaker/">SpiNNaker</a> folder: SpiNNaker implementation of the dynamic interpolation model.</p></li>
		<ul>
			<li><p align="justify"><a href="SpiNNaker/test.py">test.py</a>: runs the test of the complete network implemented in <a href="SpiNNaker/SpikingInterpolator.py">SpikingInterpolator.py</a> with the network configuration defined in <a href="SpiNNaker/spiking_interpolator_config.json">spiking_interpolator_config.json</a>.</p></li>
			<li><p align="justify"><a href="SpiNNaker/plot.py">plot.py</a>: set of utility functions used in the different scripts of the model.</p></li>
			<li><p align="justify"><a href="SpiNNaker/comparator/">comparator</a> folder: test and implementation of the comparator (following the same structure as the complete system).</p></li>
			<li><p align="justify"><a href="SpiNNaker/shifted_wta/">shifted_wta</a> folder: test and implementation of the WTA (following the same structure as the complete system)</p></li>
		</ul>
</ul>
</p>


<h2 name="Usage">Usage</h2>
<h2 name="UsageDYNAP-SE2">DYNAP-SE2</h2>
<p align="justify">
To run the model on DYNAP-SE2, it is necessary to execute <a href="DYNAP-SE2/main.py">main.py</a>. This script sets the configuration and communication of the board to be used, for which parameters <strong>profileName</strong> and <strong>bitfiles</strong> must be completed with the path to the file containing the profiling and bitfile of the board, respectively. Through parameter <strong>experiment</strong>, the component of the network to be executed is selected: 0 for the comparator, 1 for the WTA, or 2 for the complete system. Within each component's script, in the main() function, the different parameters of the model's module itself are defined, such as the number of fine and coarse-grained positions of the robot and reference, or the WTA offset.
</p>
<h2 name="UsageSpiNNaker">SpiNNaker</h2>
<p align="justify">
In SpiNNaker, it is only necessary to execute the test.py function of each module (<a href=SpiNNaker/comparator/test.py">comparator</a>, <a href="SpiNNaker/shifted_wta/test.py">wta</a> or <a href="SpiNNaker/test.py">complete system</a>) to test the model with the characteristics defined in the same script. The parameters that can be adjusted are: <strong>numPositions</strong> or the number of one-hot positions the system works with, <strong>offset</strong> or the WTA offset, <strong>simTime</strong> or the simulation duration, <strong>saveFigPath</strong> or the path where the raster plot resulting from the simulation will be stored, and the set of spiking trains that enter the network (<strong>inputRobCoarseSpikes</strong> simulating the coarse-grained position of the robot, <strong>nuinputRobFineSpikesmPositions</strong> for the fine-grained position of the robot, and <strong>inputRefSpikes</strong> for the reference position of the system).
</p>


<h2 name="CiteThisWork">Cite this work</h2>
<p align="justify">
Under construction...
</p>


<h2 name="Credits">Credits</h2>
<p align="justify">
The author of the original idea is Daniel Casanueva-Morato while working on a research project of the <a href="http://www.rtc.us.es/">RTC Group</a>.

This research was partially supported by NEKOR (PID2023-149071NB-C54) from MICIU/AEI /10.13039/501100011033 and by USECHIP (TSI-069100-2023-001) of PERTE Chip Chair program, funded by European Union – Next Generation EU. 

D. C.-M. was supported by a FPU Scholarship from the Spanish MICIU.
</p>


<h2 name="License">License</h2>
<p align="justify">
This project is licensed under the GPL License - see the <a href="https://github.com/dancasmor/Towards-Dynamic-Closed-Loop-Neuromorphic-Trajectory-Interpolation-Model/blob/main/LICENSE">LICENSE.md</a> file for details.
</p>
<p align="justify">
Copyright © 2025 Daniel Casanueva-Morato<br>  
<a href="mailto:dcasanueva@us.es">dcasanueva@us.es</a>
</p>

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)
