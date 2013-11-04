import os,sys,time

#Place these during installation 
global scriptFolder
scriptFolder = '/submissionScripts/'

global datadiskFolder 
datadiskFolder = '/data/snoplus/jonesc/analysis/'

global pysnotInstallFolder
pysnotInstallFolder = '/home/jonesc/pySNOt/'

global pysnotAnalysisFolder
pysnotAnalysisFolder = pysnotInstallFolder + str('analysisScripts/')

global ratEnvFile
ratEnvFile = str('/home/jonesc/env_rat-dev.sh')

global ratFolder
ratFolder = str('/home/jonesc/rat/')

global submissionScriptFolder 
submissionScriptFolder = str('/home/jonesc/pySNOt/batch/')


class analyscript:

    def __init__(self,batchTime,scriptName,inputFile,outputFile):
        ## Need default behaviour in case these are undefined
        self.batchTime = batchTime
        self.scriptName = scriptName
        self.inputFile = inputFile
        self.outputFile = outputFile
        
    def setTitle(self,graphTitle):
        self.graphTitle = str(graphTitle)
        self.graphTitle = str(self.graphTitle).replace(" ","")
    
    def setxaxis(self,xAxisTitle,xLow,xHigh,xBinWidth):
        self.xAxisTitle = str(xAxisTitle)
        self.xAxisTitle = str(self.xAxisTitle).replace(" ","")
        self.xLow = str(xLow)
        self.xHigh = str(xHigh)
        self.xBinWidth = str(xBinWidth)

    def setyaxis(self,yAxisTitle,yLow,yHigh):
        self.yAxisTitle = str(yAxisTitle)
        self.yAxisTitle = str(self.yAxisTitle).replace(" ","")
        self.yLow = str(yLow)
        self.yHigh = str(yHigh)
    
    def submit(self):
        print "Submit to batch for " + str(self.batchTime) + " ! \n"

        scriptFolder = datadiskFolder +  str(self.batchTime) + "_" + str(int(time.time())) + "/"
        print " scriptFolder = " + str(scriptFolder)  

        scriptFilePath = str(scriptFolder) + str(self.scriptName) + '.txt'
        print " scriptFilePath = " + str(scriptFilePath)
        
        os.system('mkdir ' + str(scriptFolder))
 
        scriptFile = open(scriptFilePath,'w')
        scriptFile.write('g++ -Wall `root-config --cflags --glibs` -o '+ str(self.scriptName) + ' -Iinclude -I' +str(ratFolder)+ 'include -Iinclude/RAT -I'+str(ratFolder)+'include/RAT -I'+str(ratFolder)+'include/RAT/DS -L'+str(ratFolder)+'lib -lHistPainter  -lRATEvent_Linux ' + str(pysnotAnalysisFolder) + str(self.scriptName) +'.C')
        scriptFile.close()
        
        scriptID = self.scriptName + "_" +str(int(time.time()))

        submissionScriptFile = str(submissionScriptFolder) +str(scriptID) + '.sh'
        
        #Test to see if the submissionScriptFolder still exsists
        pathTest =  os.path.exists(submissionScriptFolder)
        if(pathTest == True):
            pass
        else:
            os.system('mkdir '+str(submissionScriptFolder))
        
        submissionScript = open(submissionScriptFile,'w')
        submissionScript.write(' #!/bin/bash \n source ' + str(ratEnvFile)+ ' \n\n cd ' + str(scriptFolder) + '\n ./' + str(self.scriptName) + ' ' + str(self.inputFile) + ' ' + str(self.outputFile)+ ' ' + str(self.graphTitle) + ' ' + str(self.xAxisTitle) + ' ' + str(self.yAxisTitle) + ' ' + str(self.xLow) + ' ' + str(self.xHigh) + ' '+ str(self.xBinWidth) + ' ' + str(self.yLow) + ' ' +str(self.yHigh))
        submissionScript.close()
        
        ##Source the analysis submission script
        os.system('source ' + scriptFilePath)
        moveCommand = 'mv ' + str(self.scriptName) + ' ' + str(scriptFolder)
        print moveCommand
        os.system(moveCommand)
        
        ## Check to see if this is a testing job
        if(self.batchTime == "testing"):
            batchCmd = 'qsub -q testing ' +str(submissionScriptFile)
        else:
            batchCmd = 'qsub -l cput=' + self.batchTime + ' ' +str(submissionScriptFile)
        
        os.system(batchCmd)
