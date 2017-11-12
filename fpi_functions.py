# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 14:36:19 2/17

@author: Barton
"""

from math import log, ceil

def calculate_fpi_ros(fpi_term_dict):
    """
    This function takes the finals inputs from an FPI contract, calculates
        underrun/overrun, and outputs a tuple of ROS from the given inputs

    Input explanation:
        Target Cost as dollars
        Target Price as dollars
        OR Share as decimal (of the seller)
        UR Share as decimal (of the seller)
        Ceiling Percent as decimal
        Final Cost as dollars
        Unallowables optional as dollars
        FCCOM optional as dollars
        :param ref:
    """

    #These are the final results and will be output as a tuple
    ros_final = 0.0
    profit_final = 0.0

    #Calculating values used in ROS and profit calculations
    share_or_buyer = 1 - fpi_term_dict['OR Share']
    share_ur_buyer = 1 - fpi_term_dict['UR Share']
    price_ceiling = fpi_term_dict['Target Price'] * fpi_term_dict['Ceiling Percent']
    
    cost_final_billable = fpi_term_dict['Final Cost'] + fpi_term_dict['FCCOM'] - fpi_term_dict['UNALLOW']
    cost_target_delta = fpi_term_dict['Target Cost'] - fpi_term_dict['Final Cost']
    profit_target = fpi_term_dict['Target Price'] - fpi_term_dict['Target Cost']
    pta = (price_ceiling - fpi_term_dict['Target Price'])/(share_or_buyer) + fpi_term_dict['Target Cost']
    cost_before_pta = pta - fpi_term_dict['Target Cost']

    #Determining whether the final cost has underrun or overrun the target cost
    #and adjust the final profit
    if cost_target_delta > 0: #underrun
        profit_final = profit_target + cost_target_delta * fpi_term_dict['UR Share']
    elif cost_target_delta < 0: #overrun
        if cost_final_billable > pta:
            profit_final = profit_target + (pta - cost_final_billable) - (cost_before_pta * fpi_term_dict['OR Share'])
        else:
            profit_final = cost_target_delta * fpi_term_dict['OR Share'] + profit_target
    else: #final cost equal to target cost
        profit_final = profit_target

    price_contract = fpi_term_dict['Target Cost'] + profit_final

    ros_final = (price_contract - cost_final_billable)/price_contract

    return ros_final

def frange(start, end=None, inc=None):
    "A range function, that does accept float increments..."

    if end == None:
        end = start + 0.0
        start = 0.0
    else:
        end += .000001

    if inc == None:
        inc = 1.0

    L = []
    while 1:
        next = start + len(L) * inc
        if inc > 0 and next >= end:
            break
        elif inc < 0 and next <= end:
            break
        L.append(next)

    return L

#Rounds a given number to the nearest power of 10
def ceil_power_of_10(n):
    exp = log(n, 10)
    exp = ceil(exp)
    return 10**exp
    