# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 14:25:24 2017

@author: Barton

@purpose: To input a set of terms for the FPI/F defense contract type and
            generate all possible 'equivalent scenarios.' Histograms will be
            generated from the results.
"""
from fpi_functions import calculate_fpi_ros

#Initialize reference terms that all equivalent terms are generated from
cost_target_ref = 0.0
price_target_ref = 0.0
share_ur_sel_ref = 0.0
share_or_sel_ref = 0.0
ceiling_percent = 0.0


ros_test = calculate_fpi_ros(100, 113, 0.8, 0.2,
                            1.2, 102, 0.0, 0.0)

                       
                            
print(ros_test)
