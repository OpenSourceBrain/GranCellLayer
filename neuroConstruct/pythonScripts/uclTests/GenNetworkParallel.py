# -*- coding: utf-8 -*-
#
#
#   File to generate network for execution on parallel NEURON
#   Note this script has only been tested with UCL's cluster!
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

from java.io import File

from ucl.physiol.neuroconstruct.project import ProjectManager
from ucl.physiol.neuroconstruct.utils import NumberGenerator
from ucl.physiol.neuroconstruct.hpc.mpi import MpiSettings
from ucl.physiol.neuroconstruct.simulation import SimulationsInfo
from ucl.physiol.neuroconstruct.cell.utils import CellTopologyHelper

path.append(environ["NC_HOME"]+"/pythonNeuroML/nCUtils")
import ncutils as nc

projFile = File("../../GranCellLayer.ncx")


###########  Main settings  ###########

simConfig=              "Large3DNetwork"
simDuration =           500 # ms                                ##
simDt =                 0.025 # ms
neuroConstructSeed =    134623                                   ##
simulatorSeed =         234634                                   ##

simulators =             ["NEURON"]

simRefPrefix =          "T_"                               ##
suggestedRemoteRunTime = 120                                     ##

defaultSynapticDelay =  0.1 



#mpiConf =               MpiSettings.LEGION_8PROC
#mpiConf =               MpiSettings.LEGION_64PROC
mpiConf =               MpiSettings.LOCAL_SERIAL
mpiConf =               MpiSettings.MATLEM_8PROC

scale =             10                              ##


numGC =           75
numMF =            12
numGoC =           4




varTimestepNeuron =     False
verbose =               True
runInBackground=        False



#######################################


### Load neuroConstruct project


import datetime

start = datetime.datetime.now()

print "Loading project %s from at %s " % (projFile.getCanonicalPath(),start.strftime("%Y-%m-%d %H:%M"))

pm = ProjectManager()
project = pm.loadProject(projFile)


### Set duration & timestep & simulation configuration

project.simulationParameters.setDt(simDt)
simConfig = project.simConfigInfo.getSimConfig(simConfig)
simConfig.setSimDuration(simDuration)


### Set simulation reference

index = 0
simRef = "%s%i"%(simRefPrefix,index)


while File( "%s/simulations/%s_N"%(project.getProjectMainDirectory().getCanonicalPath(), simRef)).exists():
    simRef = "%s%i"%(simRefPrefix,index)
    index = index+1

project.simulationParameters.setReference(simRef)


### Change num in each cell group

numGC = int(scale * numGC)
numMF = int(scale * numMF)
numGoC = int(scale * numGoC)

project.cellGroupsInfo.getCellPackingAdapter("GrC_3D").setMaxNumberCells(numGC)
project.cellGroupsInfo.getCellPackingAdapter("MF_3D").setMaxNumberCells(numMF)
project.cellGroupsInfo.getCellPackingAdapter("GoC_3D").setMaxNumberCells(numGoC)





### Change parallel configuration

mpiSettings = MpiSettings()
simConfig.setMpiConf(mpiSettings.getMpiConfiguration(mpiConf))
print "Parallel configuration: "+ str(simConfig.getMpiConf())

if suggestedRemoteRunTime > 0:
    project.neuronFileManager.setSuggestedRemoteRunTime(suggestedRemoteRunTime)
    project.genesisFileManager.setSuggestedRemoteRunTime(suggestedRemoteRunTime)


### Change synaptic delay associated with each net conn

for netConnName in simConfig.getNetConns():
    if netConnName.count("gap")==0:
        print "Changing synaptic delay in %s to %f"%(netConnName, defaultSynapticDelay)
        delayGen = NumberGenerator(defaultSynapticDelay)
        for synProps in project.morphNetworkConnectionsInfo.getSynapseList(netConnName):
            synProps.setDelayGenerator(delayGen)

# defaultSynapticDelay will be recorded in simulation.props and listed in SimulationBrowser GUI
SimulationsInfo.addExtraSimProperty("defaultSynapticDelay", str(defaultSynapticDelay))


### Generate network structure in neuroConstruct

pm.doGenerate(simConfig.getName(), neuroConstructSeed)

while pm.isGenerating():
        print "Waiting for the project to be generated with Simulation Configuration: "+str(simConfig)
        sleep(2)


print "Generated %i cells in %i cell groups" % (project.generatedCellPositions.getNumberInAllCellGroups(), project.generatedCellPositions.getNumberNonEmptyCellGroups())
print "Generated %i instances in %i network connections" % (project.generatedNetworkConnections.getNumAllSynConns(), project.generatedNetworkConnections.getNumNonEmptyNetConns())
print "Generated %i instances in %i elect inputs" % (project.generatedElecInputs.getNumberSingleInputs(), project.generatedElecInputs.getNonEmptyInputRefs().size())


if simulators.count("NEURON")>0:
    
    simRefN = simRef+"_N"
    project.simulationParameters.setReference(simRefN)

    nc.generateAndRunNeuron(project,
                            pm,
                            simConfig,
                            simRefN,
                            simulatorSeed,
                            verbose=verbose,
                            runInBackground=runInBackground,
                            varTimestep=varTimestepNeuron)
        
    sleep(2) # wait a while before running GENESIS...
    
if simulators.count("GENESIS")>0:
    
    simRefG = simRef+"_G"
    project.simulationParameters.setReference(simRefG)

    nc.generateAndRunGenesis(project,
                            pm,
                            simConfig,
                            simRefG,
                            simulatorSeed,
                            verbose=verbose,
                            runInBackground=runInBackground)
                            
    sleep(2) # wait a while before running MOOSE...


if simulators.count("MOOSE")>0:

    simRefM = simRef+"_M"
    project.simulationParameters.setReference(simRefM)

    nc.generateAndRunMoose(project,
                            pm,
                            simConfig,
                            simRefM,
                            simulatorSeed,
                            verbose=verbose,
                            runInBackground=runInBackground)
                            
    sleep(2) # wait a while before running GENESIS...


print "Finished running all sims, shutting down..."


stop = datetime.datetime.now()
print
print "Started: %s, finished: %s" % (start.strftime("%Y-%m-%d %H:%M"),stop.strftime("%Y-%m-%d %H:%M"))
print


sleep(5)
exit()
