import pySNOt

inFile = "/data/snoplus/jonesc/batch_output/alphaDouble/alphaDouble.root"
outFile = "/data/snoplus/jonesc/longShortTruth.root"
test = pySNOt.analyscript("testing","getLSTruth",inFile,outFile)
test.setTitle("10Mev_Alpha")
test.setxaxis("QHS/QHL_PMTTruth",0.0,1500.0,10.0)
test.setyaxis("Number_of_Bins",0.0,0.0)
test.submit()
