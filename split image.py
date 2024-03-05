# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 07:51:57 2024

@author: dell
"""

import splitfolders 

input_folder = 'Data sets original/'


splitfolders.ratio(input_folder, output="Data set resize", 
                   seed=42, ratio = (.7, .15, .15), 
                    group_prefix=None) 