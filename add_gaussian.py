#!/usr/bin/python
'''
Read xcm files with the model 'tbabs*thcomp*diskbb', modify it to 'tbabs(thcomp*diskbb)smedge', fit, and save the new xcm file
By Qunfeng 2022/07
'''

import sys # to get the argument of the xcm file name
import csv
from xspec import *

csv_path = "add_gaussian_par.csv"
file = open(csv_path, 'a+', encoding='utf-8', newline='') # read the csv file

obsID = sys.argv[1] # argv = [python_filename , obsID], so the obsID is argv[1]
AllModels.setEnergies("0.001 500. 1000 log") # energies(0.001,500,1000,log)
Xset.restore(obsID+"_standard2f_0134off-corr.grp.auto_thcomp.xcm") # read xcm files

Fit.query = "yes"
Fit.perform()

Gamma_tau = AllModels(1).thcomp.Gamma_tau.values[0] # obtain values of each parameter
kT_e = AllModels(1).thcomp.kT_e.values[0]
cov_frac = AllModels(1).thcomp.cov_frac.values[0]
Tin = AllModels(1).diskbb.Tin.values[0]
norm = AllModels(1).diskbb.norm.values[0]
chi2 = Fit.statistic # obtain the chi
dof = Fit.dof

m1 = Model("tbabs(thcomp*diskbb+gaussian)smedge") # set the parameters of the new model
m1.TBabs.nH = 2.0
m1.TBabs.nH.frozen = True
m1.thcomp.Gamma_tau = Gamma_tau
m1.thcomp.kT_e = kT_e
m1.thcomp.cov_frac = cov_frac
m1.diskbb.Tin = Tin
m1.diskbb.norm = norm
m1.gaussian.LineE.values = "6.4,,6,6,7,7"
m1.gaussian.LineE.frozen = True
m1.gaussian.Sigma = 0.01
m1.gaussian.Sigma.frozen = True
m1.smedge.edgeE.values = ",,7,7,9,9"
m1.smedge.width = 7
m1.smedge.width.frozen = True

Fit.perform()
m1.gaussian.LineE.frozen = False # fit first with LineE frozen to 6.4 keV and then thaw it
Fit.perform()
Xset.parallel.error = 30 # set parallel processes in use of error command
Fit.error("max 10 1-14") # determine confidence intervals with the max chi to be 10
Fit.perform()

Gamma_tau = AllModels(1).thcomp.Gamma_tau.values[0] # obtain values of each parameter
kT_e = AllModels(1).thcomp.kT_e.values[0]
cov_frac = AllModels(1).thcomp.cov_frac.values[0]
Tin = AllModels(1).diskbb.Tin.values[0]
norm_diskbb = AllModels(1).diskbb.norm.values[0]
LineE = AllModels(1).gaussian.LineE.values[0]
norm_gaussian = AllModels(1).gaussian.norm.values[0]
edgeE = AllModels(1).smedge.edgeE.values[0]
MaxTau = AllModels(1).smedge.MaxTau.values[0]
chi2 = Fit.statistic # obtain the chi
dof = Fit.dof

Xset.save(obsID + "_thcomp.xcm", info="a") # save as obsID_thcomp.xcm

csv_writer = csv.writer(file)
# csv_writer.writerow([f'obsID', 'Gamma_tau', "kT_e", "cov_frac", "Tin", "norm", "chi2/dof"])
csv_writer.writerow([obsID, Gamma_tau, kT_e, cov_frac, Tin, norm_diskbb, LineE, norm_gaussian, edgeE, MaxTau, str(chi2) + "/" + str(dof)]) # save values of parameters in the csv file
file.close()