import pySNOt

inFile = "/data/snoplus/jonesc/batch_output/alphaDouble/alphaDouble.root"
outFile = "/data/snoplus/jonesc/batch_output/C14/output.root"
test = pySNOt.analyscript("testing","getNhits",inFile,outFile)
test.setTitle("my test value")
test.setxaxis("x axis")
test.setyaxis("y axis")
test.submit()
