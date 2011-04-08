#
#
#   File to test GranCellLayer project generation & execution without any GUI elements
#
#   Author: Padraig Gleeson
#
#   This file has been developed as part of the neuroConstruct project
#   This work has been funded by the Medical Research Council and the
#   Wellcome Trust
#
#

from sys import *
from time import *

try:
	from java.io import File
except ImportError:
	print "Note: this file should be run using ..\\..\\..\\nC.bat -python XXX.py' or '../../../nC.sh -python XXX.py'"
	print "See http://www.neuroconstruct.org/docs/python.html for more details"
	quit()

from ucl.physiol.neuroconstruct.project import ProjectManager
from ucl.physiol.neuroconstruct.neuron import NeuronFileManager
from ucl.physiol.neuroconstruct.nmodleditor.processes import ProcessManager
from ucl.physiol.neuroconstruct.utils import NumberGenerator
from ucl.physiol.neuroconstruct.simulation import SimulationsInfo
from ucl.physiol.neuroconstruct.simulation import SimulationData
from ucl.physiol.neuroconstruct.simulation import SpikeAnalyser


projFile = File("../GranCellLayer.ncx")


###########  Main settings  ###########

simConfig =            "3DNetworkModel"
simDuration =          200  # ms
simDt =                0.01 # ms
neuroConstructSeed =   1234
simulatorSeed =        1111
simRefPrefix =         "SB_"
defaultSynapticDelay = 0.2  # ms
runInBackground =      True

#######################################


# Load neuroConstruct project



print "Loading project from "+ projFile.getCanonicalPath()


pm = ProjectManager()
myProject = pm.loadProject(projFile)

myProject.simulationParameters.setDt(simDt)
index = 0

while File( "%s/simulations/%s%i"%(myProject.getProjectMainDirectory().getCanonicalPath(), simRefPrefix,index)).exists():
    index = index+1

simRef = "%s%i"%(simRefPrefix,index)
myProject.simulationParameters.setReference(simRef)



# Use this so defaultSynapticDelay will be recorded in simulation.props and listed in SimulationBrowser GUI
SimulationsInfo.addExtraSimProperty("defaultSynapticDelay", str(defaultSynapticDelay))

simConfig = myProject.simConfigInfo.getSimConfig(simConfig)

simConfig.setSimDuration(simDuration)

for netConnName in simConfig.getNetConns():
    if netConnName.count("gap")==0:
        print "----------   Changing synaptic delay in %s to %f"%(netConnName, defaultSynapticDelay)
        delayGen = NumberGenerator(defaultSynapticDelay)
        for synProps in myProject.morphNetworkConnectionsInfo.getSynapseList(netConnName):
            synProps.setDelayGenerator(delayGen)
            
for netConnName in simConfig.getNetConns():
        print myProject.morphNetworkConnectionsInfo.getSynapseList(netConnName)


pm.doGenerate(simConfig.getName(), neuroConstructSeed)

while pm.isGenerating():
        print "Waiting for the project to be generated with Simulation Configuration: "+str(simConfig)
        sleep(1)

numGenerated = myProject.generatedCellPositions.getNumberInAllCellGroups()

print "Number of cells generated: " + str(numGenerated)

for conn in myProject.generatedNetworkConnections.getSynapticConnections(simConfig.getNetConns().get(0)):
	print conn
	assert conn.props.get(0).weight >=  0.51 and conn.props.get(0).weight <= .69

print "Parallel configuration: "+ str(simConfig.getMpiConf())

if runInBackground:
    myProject.neuronSettings.setNoConsole()
else:
    myProject.neuronFileManager.setQuitAfterRun(1)

myProject.neuronFileManager.generateTheNeuronFiles(simConfig,
                                                    None,
                                                    NeuronFileManager.RUN_HOC,
                                                    simulatorSeed)

print "Generated NEURON files for: "+simRef

compileProcess = ProcessManager(myProject.neuronFileManager.getMainHocFile())

compileSuccess = compileProcess.compileFileWithNeuron(0,0)

print "Compiled NEURON files for: "+simRef

if compileSuccess:
    pm.doRunNeuron(simConfig)
    print "Set running simulation: "+simRef
    
simDir = File(projFile.getParentFile(), "/simulations/"+simRef)
timeFile = File(simDir, "time.dat")

while not timeFile.exists():
    print "Waiting for file: %s to be generated..."%timeFile.getCanonicalPath()
    sleep(2) # wait a while...

print "--- Reloading data from simulation in directory: %s"%simDir.getCanonicalPath()
sleep(1) # wait a while...

try:
    simData = SimulationData(simDir)
    simData.initialise()
    times = simData.getAllTimes()
    cellSegmentRef = simConfig.getCellGroups().get(0)+"_0"
    volts = simData.getVoltageAtAllTimes(cellSegmentRef)

    print "Got "+str(len(volts))+" data points on cell seg ref: "+cellSegmentRef

    analyseStartTime = 0
    analyseStopTime = simConfig.getSimDuration()
    analyseThreshold = -20 # mV

    spikeTimes = SpikeAnalyser.getSpikeTimes(volts, times, analyseThreshold, analyseStartTime, analyseStopTime)
    
    print "Number of spikes in %s: %i"%(cellSegmentRef, len(spikeTimes))
    avgFreq = 0.
    if len(spikeTimes)>1:
        avgFreq = len(spikeTimes)/ ((analyseStopTime - analyseStartTime)/1000.0)
    print "Firing frequency: %f Hz"%avgFreq
    
except:
    print "Error analysing simulation data from: %s"%simDir.getCanonicalPath()
    print exc_info()


exit()
