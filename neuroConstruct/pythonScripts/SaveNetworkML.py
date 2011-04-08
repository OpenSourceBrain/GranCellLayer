#
#
#   File to save network in NetworkML
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
from ucl.physiol.neuroconstruct.utils import NumberGenerator
from ucl.physiol.neuroconstruct.simulation import SimulationsInfo


projFile = File("../GranCellLayer.ncx")


###########  Main settings  ###########

simConfig =            "3DNetworkModel"
simDuration =          100  # ms
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
        print "Changing synaptic delay in %s to %i"%(netConnName, defaultSynapticDelay)
        delayGen = NumberGenerator(defaultSynapticDelay)
        for synProps in myProject.morphNetworkConnectionsInfo.getSynapseList(netConnName):
            synProps.setDelayGenerator(delayGen)


pm.doGenerate(simConfig.getName(), neuroConstructSeed)

while pm.isGenerating():
        print "Waiting for the project to be generated with Simulation Configuration: "+str(simConfig)
        sleep(1)

numGenerated = myProject.generatedCellPositions.getNumberInAllCellGroups()

print "Number of cells generated: " + str(numGenerated)


myNetworkMLFile = File("TestNetwork.nml")

pm.saveNetworkStructureXML(myProject, myNetworkMLFile, 0, 0, simConfig.getName(), "Physiological Units")

print "Network structure saved to file: "+ myNetworkMLFile.getAbsolutePath()


quit()

