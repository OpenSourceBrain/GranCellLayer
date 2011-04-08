#
#
#   A file which generates a frequency vs current curve for the Granule & Golgi cells
#   in the GranCellLayer project
#   
#   To execute this file, type '..\..\..\nC.bat -python GranGolgiF_I.py' (Windows)
#   or '../../../nC.sh -python GranGolgiF_I.py' (Linux/Mac)
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

from math import *

sys.path.append(os.environ["NC_HOME"]+"/pythonNeuroML/nCUtils")

import ncutils as nc
from ucl.physiol.neuroconstruct.hpc.mpi import MpiSettings

simConfig="Single Granule cell"


preStimDel = 0
preStimDur = 200

stimAmpLow =  0.003
stimAmpInc =  0.003
stimAmpHigh = 0.03

stimDel = preStimDur
stimDur = 1500

simDuration = preStimDur + stimDur # ms

analyseStartTime = stimDel + 100 # So it's firing at a steady rate...
analyseStopTime = simDuration
analyseThreshold = -20 # mV


mpiConfig =            MpiSettings.LOCAL_SERIAL    # Default setting: run on one local processor
#mpiConfig =            MpiSettings.MATLEM_1PROC    # Run on one processor on UCL cluster

numConcurrentSims = 4
if mpiConfig != MpiSettings.LOCAL_SERIAL: numConcurrentSims = 30
suggestedRemoteRunTime = 9   # mins



# Load neuroConstruct project

projFile = File("../GranCellLayer.ncx")


simManager = nc.SimulationManager(projFile,
                                  numConcurrentSims)

simManager.generateFICurve("NEURON",
                           simConfig,
                           stimAmpLow,
                           stimAmpInc,
                           stimAmpHigh,
                           stimDel,
                           stimDur,
                           simDuration,
                           analyseStartTime,
                           analyseStopTime,
                           analyseThreshold,
                           mpiConfig =                mpiConfig,
                           suggestedRemoteRunTime =   suggestedRemoteRunTime)



simConfig="Single Golgi Cell"


preStimDel = 0
preStimDur = 200

stimAmpLow = -0.02
stimAmpInc = 0.002
stimAmpHigh = 0.03

stimDel = preStimDur
stimDur = 3000

simDuration = preStimDur + stimDur # ms

analyseStartTime = stimDel + 200 # So it's firing at a steady rate...
analyseStopTime = simDuration


simManager.generateFICurve("NEURON",
                 simConfig,
                 stimAmpLow,
                 stimAmpInc,
                 stimAmpHigh,
                 stimDel,
                 stimDur,
                 simDuration,
                 analyseStartTime,
                 analyseStopTime,
                 analyseThreshold,
                 mpiConfig =                mpiConfig,
                 suggestedRemoteRunTime =   suggestedRemoteRunTime)