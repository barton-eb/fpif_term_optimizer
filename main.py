# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 14:25:24 2017

@author: Barton

@purpose: To input a set of terms for the FPI/F defense contract type and generate all possible 'equivalent scenarios.' Histograms
            will be generated from the results.
"""
from fpi_functions import calculate_fpi_ros

calculate_fpi_ros(100, 115, .5, .6, 120, 100, 1, 0.9)

