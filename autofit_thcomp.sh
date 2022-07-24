#!/bin/bash
'''
Automatic fitting for each pha file in the directory with the model ''tbabs*thcomp*diskbb''
use with autofit_thcomp.py to fit every grp file in the working directory 
By Qunfeng 2022/07 
'''

for obsid in *_standard2f_0134off-corr.grp
    do
        python3 autofit_thcomp.py ${obsid}
    done