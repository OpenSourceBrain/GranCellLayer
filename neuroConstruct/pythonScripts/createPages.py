#!/usr/bin/env python
'''
This is a Python script to generate a number of HTML pages displaying F-I curves of cells in this project. Work in progress
Author Yates Buckley
'''
import sys
import os
import time
import math
import shlex
import subprocess
import datetime
import re

fullbatchFlag = 0
debugFlag = 0
helpFlag = 0
for arg in sys.argv:
    if (arg == "-fullbatch"):
        fullbatchFlag = 1
    if (arg == "-debug"):
        debugFlag = 1
    if (arg == "-help"):
        helpFlag = 1

if (helpFlag == 1):
    print "run this command with ./createPages.py to batch create html pages for this project\n"+ \
    "(assuming F-I curve and V-I curve has already been generated) otherwise:\n"+ \
    "-fullbatch will run all the actual commands.. please take care it will take a long time\n"+ \
    "-debug will run the first few commands so you can test if they work\n"
    "\nnote that the script needs to be cusomised by changing actual source values..\n"
    quit()

scriptDir = "/_work/2012/neuroconstruct/neuroconstruct_svn/pythonNeuroML/nCUtils"
outputDir = "/_work/2012/neuroconstruct/neuroconstruct_svn/nCmodels/GranCellLayer/simulations"

cellArrayOutput = [\
"GranuleCell-F-I", "GranuleCell-V-I", \
"GolgiCell-F-I", "GolgiCell-V-I" ]

commandList = []

# F-I regenerate Cell1-supppyrRS-FigA1RS
commandList.append('./nCreport.sh 0 1 1 "NEURON" "/nCmodels/GranCellLayer/GranCellLayer.ncx" "singleGranuleCell" "MpiSettings.MATLEM_1PROC" 10 33  0.0 0.5 0.1 0 2000 2000  500 2000 -20  "F-I" 1 "none"')
commandList.append('./nCreport.sh 1 1 1 "NEURON" "/nCmodels/GranCellLayer/GranCellLayer.ncx" "singleGranuleCell" "MpiSettings.MATLEM_1PROC" 10 33  0.0 0.5 0.1 0 2000 2000  500 2000 -20  "F-I" 1 ')
# SS-I regenerate Cell1-supppyrRS-FigA1RS
commandList.append('./nCreport.sh 0 1 1 "NEURON" "/nCmodels/GranCellLayer/GranCellLayer.ncx" "singleGranuleCell" "MpiSettings.MATLEM_1PROC" 10 33 -3.0 2.0  0.5 0 2000 2000 1000 2000   2 "SS-I" 1 "none"')
commandList.append('./nCreport.sh 1 1 1 "NEURON" "/nCmodels/GranCellLayer/GranCellLayer.ncx" "singleGranuleCell" "MpiSettings.MATLEM_1PROC" 10 33 -3.0 2.0  0.5 0 2000 2000 1000 2000   2 "SS-I" 1 ')

# F-I regenerate Cell2-suppyrFRB-FigA1FRB
commandList.append('./nCreport.sh 0 1 1 "NEURON" "/nCmodels/GranCellLayer/GranCellLayer.ncx" "singleGolgiCell" "MpiSettings.MATLEM_1PROC" 10 33  0.0 0.5 0.1 0 2000 2000  500 2000 -20  "F-I" 1 "none"')
commandList.append('./nCreport.sh 1 1 1 "NEURON" "/nCmodels/GranCellLayer/GranCellLayer.ncx" "singleGolgiCell" "MpiSettings.MATLEM_1PROC" 10 33  0.0 0.5 0.1 0 2000 2000  500 2000 -20  "F-I" 1 ')
# SS-I regenerate Cell2-suppyrFRB-FigA1FRB
commandList.append('./nCreport.sh 0 1 1 "NEURON" "/nCmodels/GranCellLayer/GranCellLayer.ncx" "singleGolgiCell" "MpiSettings.MATLEM_1PROC" 10 33 -3.0 2.0  0.5 0 2000 2000 1000 2000   2 "SS-I" 1 "none"')
commandList.append('./nCreport.sh 1 1 1 "NEURON" "/nCmodels/GranCellLayer/GranCellLayer.ncx" "singleGolgiCell" "MpiSettings.MATLEM_1PROC" 10 33 -3.0 2.0  0.5 0 2000 2000 1000 2000   2 "SS-I" 1 ')

def a_HTML(linkText,
               linkLocation):
    html = '<a href="'+linkLocation+'">'+linkText+'</a>\n'
    return html

pageFiles = []
indexFiles = []
linkHTML = ""
imageHTML = ""

if (fullbatchFlag == 1):
    print "Running big batch of commands..."
    for i in range(len(commandList)):
        if (i % 2 == 0):
            if (debugFlag == 1 and i > 6): break
            #Popen(["/bin/bash",scriptDir+"/"+commandList[i]], cwd=scriptDir)
            cmd = commandList[i]+" \""+cellArrayOutput[i/2]+"\" "
            p = subprocess.call([cmd], cwd=scriptDir, shell=True)
            # out, err = p.communicate()
            print cmd

for i in range(len(commandList)):
    if (i % 2 == 1):
        if (debugFlag == 1 and i > 8): break
        #Popen(["/bin/bash",scriptDir+"/"+commandList[i]], cwd=scriptDir)
        cmd = commandList[i]+" \""+cellArrayOutput[i/2]+"\" "
        p = subprocess.call([cmd], cwd=scriptDir, shell=True)
        # out, err = p.communicate()
        print cmd, scriptDir
        pageFiles.append(outputDir+"/"+cellArrayOutput[i/2]+"/plot.html")
        indexFiles.append(outputDir+"/"+cellArrayOutput[i/2]+"/index.html")
        if (i % 4 == 1):
            linkHTML += '<br />'
        linkHTML += a_HTML(cellArrayOutput[i/2],"../"+cellArrayOutput[i/2]+"/index.html")

linkHTML += '<br />'

for i in range(len(pageFiles)):
    print pageFiles[i]
    plotHTML = open(pageFiles[i],'r')
    indexHTML = open(indexFiles[i],'w')
    filteredHTML = plotHTML.read()
    imageHTML = '<img src="plot.png" align="centre"/><br />'
    if (i % 2 == 1):
        imageHTML += '<img src="../'+cellArrayOutput[i-1]+'/plot.png" align="centre"/><br />'
    else:
        imageHTML += '<img src="../'+cellArrayOutput[i+1]+'/plot.png" align="centre"/><br />'

    refilteredHTML = re.sub(r'<img src="plot.png" align="centre"/>',linkHTML+imageHTML,filteredHTML)
    # re.sub(r'def\s+([a-zA-Z_][a-zA-Z_0-9]*)\s*\(\s*\):', r'static PyObject*\npy_\1(void)\n{', 'def myfunc():')

    indexHTML.write(refilteredHTML)
    indexHTML.close()
    plotHTML.close()


