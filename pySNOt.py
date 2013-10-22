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
#global ratInstallFolder 


class analyscript:

    def __init__(self,batchTime,scriptName):
        self.batchTime = batchTime
        self.scriptName = scriptName        
        
    def submit(self):
        print "Submit to batch for " + str(self.batchTime) + " ! \n"

        scriptFolder = datadiskFolder +  str(self.batchTime) + "_" + str(int(time.time())) + "/"
        print " scriptFolder = " + str(scriptFolder)  

        scriptFilePath = str(scriptFolder) + str(self.scriptName) + '.txt'
        print " scriptFilePath = " + str(scriptFilePath)
        
        os.system('mkdir ' + str(scriptFolder))
 
        scriptFile = open(scriptFilePath,'w')
        scriptFile.write('g++ -Wall `root-config --cflags --glibs` -o '+ str(self.scriptName) + ' -Iinclude -I/home/jonesc/rat/include -Iinclude/RAT -I/home/jonesc/rat/include/RAT -I/home/jonesc/rat/include/RAT/DS -L/home/jonesc/rat/lib -lHistPainter  -lRATEvent_Linux ' + str(pysnotAnalysisFolder) + str(self.scriptName) +'.C')
        scriptFile.close()
        
        scriptID = self.scriptName + str(int(time.time()))
        submissionScriptFolder = '/home/jonesc/batch/pysnot/'
        submissionScriptFile = str(submissionScriptFolder) +str(scriptID) + '.sh'
        
        #Test to see if the submissionScriptFolder still exsists
        pathTest =  os.path.exists(submissionScriptFolder)
        if(pathTest == True):
            pass
        else:
            os.system('mkdir '+str(submissionScriptFolder))
        
        print str(self.scriptName)
        submissionScript = open(submissionScriptFile,'w')
        submissionScript.write(' #!/bin/bash \n source /home/jonesc/env_rat-dev.sh \n\n cd ' + str(scriptFolder) + '\n ./' + str(self.scriptName))
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
        
        print batchCmd
