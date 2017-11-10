# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 14:36:19 2017

@author: Barton
"""

def calculate_fpi_ros(target_cost, target_price, or_share, ur_share, ceiling_percent, 
                      final_cost=0, unallow=0, fccom=0) :
    
    """
    This function takes the finals inputs from an FPI contract, calculates underrun/overrun, and outputs 
    a tuple of ROS and profit dollars from the given inputs
    """
    
    fpi_terms = {'target_cost' : target_cost, 
                 'target_price' : target_price, 
                 'or_share' : or_share,
                 'ur_share' : ur_share, 
                 'ceiling_percent' : ceiling_percent
                 }
    
    for key, val in fpi_terms.items() :
        print(key + ' : ' + str(val))
    
    