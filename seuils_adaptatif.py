# -*- coding: utf-8 -*-
"""
Created on Wed May 22 21:14:34 2019

@author: Antoine
"""

#%% 

import glob
import pandas as pd
import os

raw_path = os.path.join("Results", "raw")
fichiers = ["Adaptive_AM_and_FM_S*.dat", "Discrimination1_AM_and_FM_S*.dat"]

adapt = glob.glob(os.path.join(raw_path,fichiers[0]))
discrimination = glob.glob(os.path.join(raw_path,fichiers[1]))

clean_adapt = pd.DataFrame()
clean_discr = pd.DataFrame()

#adaptatif
for file_name in adapt:
    split = file_name.split(sep="_")
    subject_name = split[-1].split(sep=".")[0][1:]
    
    table = pd.read_csv(file_name, sep="   ")
    table = table.iloc[:,3:5]
    table.columns = ["modulation_type", "seuil"]
    table["subject"] = [subject_name for i in range(len(table))]
    table = table[["subject","modulation_type", "seuil"]]
    
    clean_adapt = pd.concat([clean_adapt, table], ignore_index=True)
    
#discrimination
for file_name in discrimination:
    split = file_name.split(sep="_")
    subject_name = split[-1].split(sep=".")[0][1:]
    
    table = pd.read_csv(file_name, sep="   ")
    table = table.iloc[:,3:5]
    table.columns = ["modulation_type", "seuil"]
    table["subject"] = [subject_name for i in range(len(table))]
    table = table[["subject","modulation_type", "seuil"]]
    
    clean_discr = pd.concat([clean_discr, table], ignore_index=True)

clean_adapt.subject= clean_adapt.subject.astype("int")
clean_adapt = clean_adapt.sort_values(by="subject")
clean_adapt = clean_adapt.reset_index()
clean_adapt.to_csv("seuils_adaptatifs.txt")
#clean_adapt.to_excel("seuils_adaptatifs.xlsx")

clean_discr.subject= clean_discr.subject.astype("int")
clean_discr = clean_discr.sort_values(by="subject")
clean_discr = clean_discr.reset_index()
clean_discr.to_csv("seuils_discrimination.txt")
#clean_discr.to_excel("seuils_discrimination.xlsx")