# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 14:36:19 2/17

@author: Barton
"""

def calculate_fpi_ros(cost_target, price_target, share_ur_seller, share_or_seller,
                      ceiling_percent, cost_final=0, unallow=0, fccom=0):

    """
    This function takes the finals inputs from an FPI contract, calculates
        underrun/overrun, and outputs a tuple of ROS and profit dollars from
        the given inputs

    Input explanation:
        Target Cost as dollars
        Target Price as dollars
        OR Share as decimal (of the seller)
        UR Share as decimal (of the seller)
        Ceiling Percent as decimal
        Final Cost as dollars
        Unallowables optional as dollars
        FCCOM optional as dollars
    """

    #These are the final results and will be output as a tuple
    ros_final = 0.0
    profit_final = 0.0

    #Calculating values used in ROS and profit calculations
    share_or_buyer = 1 - share_or_seller
    share_ur_buyer = 1 - share_ur_seller
    price_ceiling = price_target * ceiling_percent
    
    cost_final_billable = cost_final + fccom - unallow
    cost_target_delta = cost_target - cost_final
    profit_target = price_target - cost_target
    pta = (price_ceiling - price_target)/(share_or_buyer) + cost_target
    cost_before_pta = pta - cost_target

    #Determining whether the final cost has underrun or overrun the target cost
    #and adjust the final profit
    if cost_target_delta < 0: #underrun
        profit_final = profit_target + cost_target_delta * share_ur_seller
    elif cost_target_delta > 0: #overrun
        if cost_final_billable > pta:
            profit_final = profit_target + (pta - cost_final_billable) - (cost_before_pta * share_or_seller)
        else:
            profit_final = cost_target_delta * share_or_seller + profit_target
    else: #final cost equal to target cost
        profit_final = profit_target

    price_contract = cost_target + profit_final

    ros_final = (price_contract - cost_final_billable)/price_contract

    return profit_final, ros_final
    