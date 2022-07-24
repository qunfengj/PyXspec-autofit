#!/bin/bash
'''
Automatic fitting for each pha file in the directory with the model tbabs(cutoffpl+diskbb+gaussian)*smedge
use with autofit_cutoffpl.py to fit every grp file in the working directory 
By Qunfeng 2022/07 
'''

for obsid in *_standard2f_0134off-corr.grp
    do
        python3 autofit_cutoffpl.py ${obsid}
    done