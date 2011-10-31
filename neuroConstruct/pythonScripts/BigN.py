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

import sys
import os
import time
import math


try:
    from java.io import File
except ImportError:
    print "Note: this file should be run using ..\\..\\..\\nC.bat -python XXX.py' or '../../../nC.sh -python XXX.py'"
    print "See http://www.neuroconstruct.org/docs/python.html for more details"
    quit()

sys.path.append(os.environ["NC_HOME"]+"/pythonNeuroML/nCUtils")

from ucl.physiol.neuroconstruct.hpc.mpi import MpiSettings
from ucl.physiol.neuroconstruct.simulation import SimulationData
from ucl.physiol.neuroconstruct.simulation import SimulationsInfo

import ncutils as nc # Many useful functions such as SimManager.runMultipleSims found here

projFile = File("../GranCellLayer.ncx")


###########  Main settings  ###########
simDuration =           100 # ms
simDt =                 0.025 # ms
neuroConstructSeed =    98781234
simulatorSeed =         9718111
simulators =            ["NEURON"]
simConfigs = []
simConfigs.append("TestScaling")


mpiConfigs =              [MpiSettings.MATLEM_1PROC, MpiSettings.MATLEM_2PROC, MpiSettings.MATLEM_4PROC, \
                           MpiSettings.MATLEM_8PROC, MpiSettings.MATLEM_16PROC,MpiSettings.MATLEM_32PROC,MpiSettings.MATLEM_64PROC, MpiSettings.MATLEM_128PROC, MpiSettings.MATLEM_216PROC]
#mpiConfigs =              [MpiSettings.LOCAL_SERIAL]
#mpiConfigs =              [MpiSettings.MATLEM_16PROC,MpiSettings.MATLEM_32PROC, MpiSettings.MATLEM_64PROC]
mpiConfigs =              [MpiSettings.MATLEM_32PROC]
mpiConfigs =              [MpiSettings.MATLEM_4PROC, MpiSettings.MATLEM_8PROC, MpiSettings.MATLEM_16PROC,MpiSettings.MATLEM_32PROC, MpiSettings.MATLEM_64PROC, MpiSettings.MATLEM_128PROC]
mpiConfigs =              ["MATTHAU_8","MATTHAU_16", "MATTHAU_24"]
mpiConfigs =              ["LEMMON_8","LEMMON_16", "LEMMON_24", "LEMMON_32", "LEMMON_40"]
mpiConfigs =              [MpiSettings.MATLEM_8PROC, MpiSettings.MATLEM_16PROC,MpiSettings.MATLEM_32PROC, MpiSettings.MATLEM_48PROC, MpiSettings.MATLEM_64PROC, \
                           MpiSettings.MATLEM_96PROC, MpiSettings.MATLEM_128PROC, MpiSettings.MATLEM_160PROC, MpiSettings.MATLEM_192PROC]
mpiConfigs =              [MpiSettings.MATLEM_32PROC]


#######numb = 16
###mpiConfigs =              [MpiSettings.MATLEM_48PROC]
###mpiConfigs =              ["MATTHAU_%i"%numb]
#mpiConfigs =              ["LEMMON_%i"%numb]

confs = {}
wait = True

################################
'''
pre="LEMMON_"
confs[8] = pre+str(8)
confs[16] = pre+str(16)
confs[32] = pre+str(32)
confs[48] = pre+str(48)
confs[64] = pre+str(64)
confs[80] = pre+str(80)
confs[96] = pre+str(96)
confs[112] = pre+str(112)

confs[128] = pre+str(128)
confs[144] = pre+str(144)
'''
##############################
'''
confs[48] = MpiSettings.MATLEM_48PROC

'''

confs[8] = MpiSettings.MATLEM_8PROC
confs[16] = MpiSettings.MATLEM_16PROC
confs[32] = MpiSettings.MATLEM_32PROC
confs[48] = MpiSettings.MATLEM_48PROC
confs[64] = MpiSettings.MATLEM_64PROC
confs[96] = MpiSettings.MATLEM_96PROC
confs[128] = MpiSettings.MATLEM_128PROC
confs[160] = MpiSettings.MATLEM_160PROC
confs[200] = MpiSettings.MATLEM_200PROC


wait = False

multipleRuns =          [-1, -2, -3, -4]
multipleRuns =          [-1]

suggestedRemoteRunTime = 1020   # mins

varTimestepNeuron =     False

analyseSims =           True
plotSims =              True
plotVoltageOnly =       True


runInBackground =       True

verbose =               True
runSims =               True
#runSims =               False

saveAsHdf5 =            True
#saveAsHdf5 =            False

saveOnlySpikes =        True
#saveOnlySpikes =        False

from ucl.physiol.neuroconstruct.neuron import NeuronFileManager
runMode = NeuronFileManager.RUN_HOC
#runMode = NeuronFileManager.RUN_PYTHON_XML


numConcurrentSims = 30

#######################################

def testAll(argv=None):
    if argv is None:
        argv = sys.argv

    print "Loading project from "+ projFile.getCanonicalPath()


    simManager = nc.SimulationManager(projFile,
                                      numConcurrentSims = numConcurrentSims,
                                      verbose = verbose)

    ### Change num in each cell group

    densityGrC = 1.90e6
    densityMF = 6.6e5
    densityGoC = 4607

    totDens = densityGrC + densityMF + densityGoC


    for conf in confs.keys():

        numb = conf
        mpiConfigs = [confs[conf]]

        perProc = 5000
        targetNum = perProc*numb

        simAllPrefix =          "NZ_%i_%i_"%(perProc, numb)   # Adds a prefix to simulation reference

        print "Simulation pref: "+simAllPrefix


        numMF = int(targetNum * densityMF/totDens)
        numGoC = int(targetNum * densityGoC/totDens)
        numGrC = targetNum - numMF - numGoC

        vol = targetNum/(totDens*1e-9)
        height = 150
        side = math.sqrt(vol/height)


        info = "Number in %fx%fx%i box (vol: %f mm^3): GrC: %i, MF: %i, GoC: %i, Total: %i"%(side, side, height, vol*1e-9,numGrC, numMF,numGoC, (numGrC +numMF +numGoC))
        print info

        SimulationsInfo.addExtraSimProperty("summary", info)

        region3D = simManager.project.regionsInfo.getRegionObject("TestGranCellVolume")
        region3D.setParameter(region3D.WIDTH_PARAM, side)
        region3D.setParameter(region3D.HEIGHT_PARAM, height)
        region3D.setParameter(region3D.DEPTH_PARAM, side)

        simManager.project.cellGroupsInfo.getCellPackingAdapter("TestScalingGrC").setMaxNumberCells(numGrC)
        simManager.project.cellGroupsInfo.getCellPackingAdapter("TestScalingGoC").setMaxNumberCells(numGoC)
        simManager.project.cellGroupsInfo.getCellPackingAdapter("TestScalingMF").setMaxNumberCells(numMF)
        ######simManager.project.cellGroupsInfo.getCellPackingAdapter("lg2").setMaxNumberCells(numCells2)


        allSims = simManager.runMultipleSims(simConfigs =             simConfigs,
                                   simDt =                   simDt,
                                   simDuration =             simDuration,
                                   simulators =              simulators,
                                   runInBackground =         runInBackground,
                                   varTimestepNeuron =       varTimestepNeuron,
                                   mpiConfigs =              mpiConfigs,
                                   suggestedRemoteRunTime =  suggestedRemoteRunTime,
                                   simRefGlobalPrefix =      simAllPrefix,
                                   runSims =                 runSims,
                                   maxElecLens =             multipleRuns,
                                   saveAsHdf5 =              saveAsHdf5,
                                   saveOnlySpikes =          saveOnlySpikes,
                                   runMode =                 runMode)

        if wait:
            while (len(simManager.allRunningSims)>0):
                print "Waiting for the following sims to finish: "+str(simManager.allRunningSims)
                time.sleep(30) # wait a while...
                simManager.updateSimsRunning()

            times = []
            procNums = []
            for sim in allSims:
                simDir = File(projFile.getParentFile(), "/simulations/"+sim)
                try:
                    simData = SimulationData(simDir)
                    simData.initialise()
                    simTime = simData.getSimulationProperties().getProperty("RealSimulationTime")
                    print "Simulation: %s took %s seconds"%(sim, simTime)
                    times.append(float(simTime))
                    paraConfig = simData.getSimulationProperties().getProperty("Parallel configuration")
                    print paraConfig
                    numProc = int(paraConfig[max(paraConfig.find(" host, ")+7, paraConfig.find(" hosts, ")+8):paraConfig.find(" processor")])
                    procNums.append(numProc)

                except:
                    print "Error analysing simulation data from: %s"%simDir.getCanonicalPath()
                    print sys.exc_info()




if __name__ == "__main__":
    testAll()
