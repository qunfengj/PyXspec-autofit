#!/usr/bin/python
'''
Read xcm files with the model 'tbabs*thcomp*diskbb' and save the values for each parameter in csv files
By Qunfeng 2022/07
'''

import sys # to get the argument of the xcm file name
import csv
from xspec import *

csv_path = "par_nonrefl.csv"
file = open(csv_path, 'a+', encoding='utf-8', newline='') # read the csv file

xcmname = sys.argv[1] # argv = [python_filename , xcmname], so the xcm file is argv[1]
AllModels.setEnergies("0.001 500. 1000 log") # energies(0.001,500,1000,log)
Xset.restore(xcmname) # read xcm files

Fit.query = "yes"
Fit.perform()

Gamma_tau = AllModels(1).thcomp.Gamma_tau.values[0] # obtain values of each parameter
kT_e = AllModels(1).thcomp.kT_e.values[0]
cov_frac = AllModels(1).thcomp.cov_frac.values[0]
Tin = AllModels(1).diskbb.Tin.values[0]
norm = AllModels(1).diskbb.norm.values[0] # obtain the chi
chi2 = Fit.statistic
dof = Fit.dof

class Nstr: # define a new class to do string minus calculations
    def __init__(self, arg):
       self.x=arg
    def __sub__(self,other):
        c=self.x.replace(other.x,"")
        return c

xcm_Nstr = Nstr(xcmname)
file_end_Nstr = Nstr("_standard2f_0134off-corr.grp.auto_thcomp.xcm")
obsID = xcm_Nstr - file_end_Nstr # do string minus calculations

csv_writer = csv.writer(file)
# csv_writer.writerow([f'obsID', 'Gamma_tau', "kT_e", "cov_frac", "Tin", "norm", "chi2/dof"])
csv_writer.writerow([obsID, Gamma_tau, kT_e, cov_frac, Tin, norm, str(chi2) + "/" + str(dof)]) # save values of parameters in the csv file
file.close()