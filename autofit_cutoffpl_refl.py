#!/usr/bin/python
'''
Automatic fitting for each pha file in the directory with the model 'tbabs(cutoffpl+diskbb+gaussian)*smedge'
By Qunfeng 2022/07
'''

import sys # to get the argument of the pha file name
from xspec import *

phaname = sys.argv[1] # argv = [python_filename , phaname], so the spectrum file is argv[1]
print(phaname)

Spectrum(phaname)
AllData.ignore("1-4,45.0-**") # ignore RXTE band 1-4(channel) and 45.0-**(keV)
Xset.abund = "wilm" # abund wilm
m1 = Model("TBabs(cutoffpl + diskbb + gaussian)smedge") # phenomenological fitting for reflection modelling

tbabs = m1.TBabs
gaussian = m1.gaussian
smedge = m1.smedge

tbabs.nH = 2.0
tbabs.nH.frozen = True # NH is set to 2.0 due to the lack of data in low energy bands and results from other telescopes and radio bands of H 1743-322
gaussian.LineE.values = ",,6,6,7,7" # LineE range is set to [6, 7]
smedge.edgeE.values = ",,7,7,9,9" # edgeE range is set to [7, 9]
smedge.width = 7.0
smedge.width.frozen = True

AllModels.setEnergies("0.01 500. 1000 log") # energies(0.001,500,1000,log)

Fit.query = "yes"
Fit.perform()

xcmname = phaname + ".auto_cutoffpl_refl.xcm"
Xset.save(xcmname, info="a") # save all xcmname