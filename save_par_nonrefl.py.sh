#!/bin/bash
'''
Read xcm files with the model tbabs*thcomp*diskbb and save the values for each parameter in csv files
use with save_par_nonrefl.py to fit every grp file in the working directory 
By Qunfeng 2022/07 
'''

for obsid in *_standard2f_0134off-corr.grp.auto_thcomp.xcm
    do
        python3 save_par_nonrefl.py ${obsid}
    done