import pySNOt

inFile = "/data/snoplus/jonesc/batch_output/alphaDouble/alphaDouble.root"
outFile = "/data/snoplus/jonesc/batch_output/C14/output.root"
test = pySNOt.analyscript("testing","getNhits",inFile,outFile)
test.setTitle("my test value")
test.setxaxis("x axis",0.0,1500.0,10.0)
test.setyaxis("y axis",0.0,1000.0)
test.submit()
