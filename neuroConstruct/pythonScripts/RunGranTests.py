#
#
#   File to test behaviour of the Granule Cell.
#
#   To execute this type of file, type '..\..\..\nC.bat -python XXX.py' (Windows)
#   or '../../../nC.sh -python XXX.py' (Linux/Mac). Note: you may have to update the
#   NC_HOME and NC_MAX_MEMORY variables in nC.bat/nC.sh
#
#   Author: Padraig Gleeson
#
#   This file has been developed as part of the neuroConstruct project
#   This work has been funded by the Medical Research Council and the
#   Wellcome Trust
#
#

import sys
import os

try:
	from java.io import File
except ImportError:
	print "Note: this file should be run using ..\\..\\..\\nC.bat -python XXX.py' or '../../../nC.sh -python XXX.py'"
	print "See http://www.neuroconstruct.org/docs/python.html for more details"
	quit()

sys.path.append(os.environ["NC_HOME"]+"/pythonNeuroML/nCUtils")

import ncutils as nc
from ucl.physiol.neuroconstruct.hpc.mpi import MpiSettings

projFile = File(os.getcwd(), "../GranCellLayer.ncx")


##############  Main settings  ##################

simConfigs = []

#simConfigs.append("Default Simulation Configuration")
simConfigs.append("Single Granule cell")

simDt =                 0.001

simulators =            ["NEURON", "GENESIS_PHYS", "GENESIS_SI", "MOOSE_PHYS", "MOOSE_SI"]
#simulators =            ["NEURON"]

varTimestepNeuron =     True
varTimestepTolerance =  0.00001

mpiConfig =            MpiSettings.LOCAL_SERIAL    # Default setting: run on one local processor
#mpiConfig =            MpiSettings.MATLEM_1PROC    # Run on one processor on UCL cluster

numConcurrentSims = 3
if mpiConfig != MpiSettings.LOCAL_SERIAL: numConcurrentSims = 5
suggestedRemoteRunTime = 2   # mins

plotSims =              True
plotVoltageOnly =       True
runInBackground =       True
analyseSims =           True
verbose =               True

#############################################


def testAll(argv=None):
    if argv is None:
        argv = sys.argv

    print "Loading project from "+ projFile.getCanonicalPath()


    simManager = nc.SimulationManager(projFile,
                                      numConcurrentSims = numConcurrentSims,
                                      verbose = verbose)


    simManager.runMultipleSims(simConfigs =               simConfigs,
                               simDt =                    simDt,
                               simulators =               simulators,
                               runInBackground =          runInBackground,
                               varTimestepNeuron =        varTimestepNeuron,
                               varTimestepTolerance =     varTimestepTolerance,
                               mpiConfig =                mpiConfig,
                               suggestedRemoteRunTime =   suggestedRemoteRunTime)

    simManager.reloadSims(plotVoltageOnly =   plotVoltageOnly,
                          analyseSims =       analyseSims)

    # These were discovered using analyseSims = True above.
    # They need to hold for all simulators
    spikeTimesToCheck = {'SingleGranule_0': [108.25, 135.861, 161.793, 187.234, 212.362, \
                                    237.349, 262.302, 287.2, 312.079, 336.969, \
                                    361.881, 386.779, 411.68, 436.46, 461.4, \
                                    486.3, 511.2, 536.1, 561.05, 586]}

    spikeTimeAccuracy = 0.1

    report = simManager.checkSims(spikeTimesToCheck = spikeTimesToCheck,
                                  spikeTimeAccuracy = spikeTimeAccuracy)

    print report

    return report


if __name__ == "__main__":
    testAll()

