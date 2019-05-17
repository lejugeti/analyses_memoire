# -*- coding: utf-8 -*-
"""
Created on Wed May  1 15:55:49 2019

@author: Antoine
"""

#%% anova pingouin

import pingouin as pg
import pandas as pd

data = pd.read_csv("aggregated_data.txt")
data = data[data.ISI<6]

aov = pg.rm_anova(dv="d", within=["modulation_type", "ISI"], 
                  subject="subject", data=data)


pg.print_table(aov)

clean_aov = aov[["Source","ddof1", "F", "p-unc", "p-GG-corr", "np2"]]
clean_aov.columns = ["Variable", "ddl", "F-value", "p-value", "p-value corrigee", "partial eta-square"]
clean_aov.to_excel("resultats_anova.xlsx")



#%% anova stats model MARCHE PAS 

from statsmodels.stats.anova import AnovaRM
import pandas as pd

data = pd.read_csv("aggregated_data.txt")
data = data[data.ISI<6]
aov2 = AnovaRM(data=data, depvar="percentage_correct", 
               subject="subject", within=["ISI", "modulation_type"]).fit()