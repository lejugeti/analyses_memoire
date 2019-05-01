# -*- coding: utf-8 -*-
"""
Created on Wed May  1 15:55:49 2019

@author: Antoine
"""

#%% anova pingouin

import pingouin as pg
import pandas as pd

data = pd.read_csv("aggregated_data.txt")
data[(data["subject"]==2)+ (data["subject"]==3)]

aov = pg.rm_anova(dv="percentage_correct", within=["modulation_type", "ISI"], 
                  subject="subject", data=data)


pg.print_table(aov)






#%% anova stats model MARCHE PAS 

from statsmodels.stats.anova import AnovaRM
import pandas as pd

data = pd.read_csv("aggregated_data.txt")
data[(data["subject"]==2)+ (data["subject"]==3)]
aov2 = AnovaRM(data=data, depvar="percentage_correct", 
               subject="subject", within=["ISI", "modulation_type"]).fit()