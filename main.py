# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 14:25:24 2017

@author: Eric Barton

@purpose: To input a set of terms for the FPI/F defense contract type and
            generate all possible 'equivalent scenarios.' Histograms will be   
            generated from the results.
"""
from fpi_functions import calculate_fpi_ros, frange, ceil_power_of_10

import pandas as pd
import matplotlib.pyplot as plt

# Init cost determination terms for seller
cost_nom_sel = 100.0
cost_con_sel = 120.0
cost_fccom = 1.0
cost_unallow = 0.9

# Init cost determination terms for buyer
cost_nom_buy = 92.0

# Choose buyer or seller as goal and set ros goal min and max if necessary
seller_is_goal = True
ros_is_range = False
ros_goal_min = 0.12
ros_goal_max = 0.135

# Init reference terms that all equivalent terms are generated from
cost_target_ref = 100.0
price_target_ref = 114.0
share_ur_sel_ref = 0.80
share_or_sel_ref = 0.20
ceiling_percent_ref = 1.20

# Init calculated terms from reference terms
profit_target_ref = price_target_ref - cost_target_ref
fee_target_ref = profit_target_ref / cost_target_ref

# Init constraints that the FPI terms must obey
cost_target_min = round((cost_nom_sel / cost_con_sel) * cost_nom_sel, 1)
cost_target_max = round(cost_con_sel, 1)
fee_target_min = 0.09
fee_target_max = 0.14
price_target_min = round(cost_target_min * (1 + fee_target_min), 1)
price_target_max = round(cost_target_max * (1 + fee_target_max), 1)
share_ur_sel_min = 0.15
share_ur_sel_max = 0.85
share_or_sel_min = 0.15
share_or_sel_max = 0.85
ceiling_percent_min = 1.10
ceiling_percent_max = 1.30

# Init Increments that the terms must obey (except for the seek term)
cost_target_inc = ceil_power_of_10(cost_target_ref) / 1000
share_ur_sel_inc = 0.05
share_or_sel_inc = 0.05
ceiling_percent_inc = 0.02
fee_target_inc = 0.001
ros_goal_inc = 0.001

if seller_is_goal:
    fpi_terms_sel_ref = {'Target Cost': cost_target_ref,
                         'Target Price': price_target_ref,
                         'UR Share': share_ur_sel_ref,
                         'OR Share': share_or_sel_ref,
                         'Ceiling Percent': ceiling_percent_ref,
                         'Final Cost': cost_nom_sel,
                         'UNALLOW': cost_unallow,
                         'FCCOM': cost_fccom
                         }
    ros_goal = calculate_fpi_ros(fpi_terms_sel_ref)
    if not ros_is_range:
        ros_goal_min = ros_goal
        ros_goal_max = ros_goal
    cost_final_test = cost_nom_sel
    cost_unallow_test = cost_unallow
    cost_fccom_test = cost_fccom

else:
    fpi_terms_buy_ref = {'Target Cost': cost_target_ref,
                         'Target Price': price_target_ref,
                         'UR Share': share_ur_sel_ref,
                         'OR Share': share_or_sel_ref,
                         'Ceiling Percent': ceiling_percent_ref,
                         'Final Cost': cost_nom_buy,
                         'UNALLOW': 0.0,
                         'FCCOM': 0.0
                         }
    ros_goal = calculate_fpi_ros(fpi_terms_buy_ref)
    if not ros_is_range:
        ros_goal_min = ros_goal
        ros_goal_max = ros_goal
    cost_final_test = cost_nom_buy
    cost_unallow_test = 0.0
    cost_fccom_test = 0.0

# List that will hold valid sets
valid_terms = {'Target Cost': [],
               'Target Price': [],
               'UR Share': [],
               'OR Share': [],
               'Ceiling Price': []}
df_valid_terms = pd.DataFrame(columns=['Target Cost',
                                       'Target Price',
                                       'UR Share',
                                       'OR Share',
                                       'Ceiling Price',
                                       'Target Fee',
                                       'Final ROS',
                                       'Buyer NOM ROS'
                                       ])

# List that will hold each test set
term_test_set = {'target cost': cost_target_min,
                 'target price': price_target_min,
                 'ur share': share_ur_sel_min,
                 'or share': share_or_sel_min,
                 'ceiling price': ceiling_percent_min}



# Function to add to the list of terms so the below is not cluttered
def add_valid_terms_to_df(test_set_dict, index):
    df_valid_terms.loc[index] = [test_set_dict['Target Cost'],
                                test_set_dict['Target Price'],
                                test_set_dict['UR Share'],
                                test_set_dict['OR Share'],
                                test_set_dict['Ceiling Percent'],
                                test_set_dict['Target Fee'],
                                test_set_dict['Final ROS'],
                                test_set_dict['Buyer NOM ROS']
                             ]

def test_set_ros(test_set_dict):
    goal_ros_round = round(test_set_dict['Goal ROS'], 4)
    test_ros_round = round(calculate_fpi_ros(test_set_dict), 4)
    return goal_ros_round==test_ros_round


test_set = {'Target Cost': term_test_set['target cost'],
            'Target Price': term_test_set['target price'],
            'UR Share': term_test_set['ur share'],
            'OR Share': term_test_set['or share'],
            'Ceiling Percent': term_test_set['ceiling price'],
            'Final Cost': cost_final_test,
            'UNALLOW': cost_unallow_test,
            'FCCOM': cost_fccom_test,
            'Goal ROS': ros_goal,
            'Final ROS' : 0.0,
            'Target Fee' : 0.0,
            'Buyer NOM ROS' : 0.0
            }

index = 0
for ros_goal_test in frange(ros_goal_min,
                            ros_goal_max,
                            ros_goal_inc):
    test_set['Goal ROS'] = ros_goal_test

    for fee_target_test in frange(fee_target_min,
                                  fee_target_max + fee_target_inc,
                                  fee_target_inc):
        print('Target Fee: ' + str(round(fee_target_test*100,2)) + ' , Current ROS Goal: ' + str(round(ros_goal_test*100,2)))

        for cost_target_test in frange(cost_target_min,
                                       cost_target_max + cost_target_inc,
                                       cost_target_inc):

            test_set['Target Cost'] = round(cost_target_test, 3)
            test_set['Target Price'] = round(cost_target_test * (1 + fee_target_test), 3)

            if test_set['Final Cost'] < test_set['Target Cost']:
                is_underrun = True
            else:
                is_underrun = False

            if is_underrun:
                for share_ur_test in frange(share_ur_sel_min,
                                            share_ur_sel_max + share_ur_sel_inc,
                                            share_ur_sel_inc):
                    test_set['UR Share'] = round(share_ur_test, 2)
                    if test_set_ros(test_set):
                        for share_or_test in frange(share_or_sel_min,
                                                    share_or_sel_max + share_or_sel_inc,
                                                    share_or_sel_inc):
                            test_set['OR Share'] = share_or_test
                            for ceiling_percent_test in frange(ceiling_percent_min,
                                                               ceiling_percent_max + ceiling_percent_inc,
                                                               ceiling_percent_inc):
                                test_set['Ceiling Percent'] = round(ceiling_percent_test, 2)
                                test_set['Final ROS'] = calculate_fpi_ros(test_set)
                                test_set['Target Fee'] = (test_set['Target Price'] - test_set['Target Cost'])/test_set['Target Cost']

                                #Temporarily switch final cost to buyer cost to get buyer ros
                                test_set['Final Cost'] = cost_nom_buy
                                test_set['Buyer NOM ROS'] = calculate_fpi_ros(test_set)
                                test_set['Final Cost'] = cost_nom_sel
                                add_valid_terms_to_df(test_set, index)
                                index += 1
            else:
                for share_or_test in frange(share_or_sel_min,
                                            share_or_sel_max,
                                            share_or_sel_inc):
                    test_set['OR Share'] = round(share_or_test, 2)
                    for ceiling_percent_test in frange(ceiling_percent_min,
                                                     ceiling_percent_max + ceiling_percent_inc,
                                                     ceiling_percent_inc):
                        test_set['Ceiling Percent'] = round(ceiling_percent_test, 2)
                        if test_set_ros(test_set):
                            for share_ur_test in frange(share_ur_sel_min,
                                                        share_ur_sel_max + share_ur_sel_inc,
                                                        share_ur_sel_inc):
                                test_set['UR Share'] = round(share_ur_test, 2)
                                test_set['Final ROS'] = calculate_fpi_ros(test_set)
                                test_set['Target Fee'] = (test_set['Target Price'] - test_set['Target Cost'])/test_set['Target Cost']
                                #Temporarily switch final cost to buyer cost to get buyer ros
                                test_set['Final Cost'] = cost_nom_buy
                                test_set['Buyer NOM ROS'] = calculate_fpi_ros(test_set)
                                test_set['Final Cost'] = cost_nom_sel
                                add_valid_terms_to_df(test_set, index)
                                index += 1

plt.scatter(x=df_valid_terms['Target Fee'], y=df_valid_terms['Buyer NOM ROS'])
plt.show()

