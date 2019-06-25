# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 08:26:31 2019

@author: Antoine
"""
#%% cleaning the matlab data
import pandas as pd
import os
import glob
import numpy as np

raw_path = os.path.join("Results", "raw", "Discrimination2_CS_AM_and_FM_ISI*.dat")

for filename in glob.glob(raw_path):
    with open(filename) as file:
        a = file.readlines()
        res = []
        for line in a:
            res.append(line.split(sep="   "))

    data = pd.DataFrame(res[1:], columns=res[0])
    data = data[["exppar3[N/A]", "n.pres", "n.correct calscript"]]
    data.columns = ["modulation_type", "nb_presentation", "nb_correct"]
    
    #change type
    data["nb_presentation"] = data["nb_presentation"].astype("int64")
    data["nb_correct"] = data["nb_correct"].astype("int64")
    data["modulation_type"] = data["modulation_type"].astype("category")
    
    #taking only non null values
    clean_data = data[data["nb_correct"]!=0]
    
    #drop arg to not insert index in dataframe when reseting
    clean_data.reset_index(drop=True, inplace=True)
    
    splitted_names = filename.split(sep="_")
    clean_data["ISI"] = [splitted_names[-2][-1] for i in range(len(clean_data))]
    clean_data = clean_data[["modulation_type", "ISI", "nb_presentation", "nb_correct"]]
    clean_data.index.name = "index"
    clean_data["subject"] = [splitted_names[-1].split(sep=".")[0][1:] for i in range(len(clean_data))]
    
    #on split une deuxième fois pour enlever le .dat qui restait après 1er split
    clean_data.to_csv(os.path.join('Results', 'clean', 
                                   f"{splitted_names[-2]}_{splitted_names[-1].split(sep='.')[0]}.txt"))

#%% building the aggregated dataframe thanks to the cleaned files
clean_path = os.path.join("Results", "clean")

clean_agg = pd.DataFrame()
for filename in os.listdir(clean_path):
    data = pd.read_csv(os.path.join(clean_path, filename), index_col="index")
    clean_agg = pd.concat([clean_agg, data], ignore_index=True)

clean_agg[["modulation_type", "subject", "ISI"]] = clean_agg[["modulation_type", "subject", "ISI"]].astype("category")

#build new dataframe with sumed correct for each subject MT and ISI
sum_presented = clean_agg.groupby(["subject", "modulation_type",  "ISI"])["nb_presentation"].apply(sum)
sum_correct = clean_agg.groupby(["subject", "modulation_type", "ISI"])["nb_correct"].apply(sum)

tidy_data = pd.DataFrame({"presented":sum_presented, "correct":sum_correct})

#colonne du percentage correct
tidy_data["percentage_correct"] = round(100 * tidy_data.correct / tidy_data.presented)

#création colonne des d'
ref_d = pd.read_excel("table_d.xlsx")
d = []
for percentage in tidy_data.percentage_correct:
    d.append(ref_d[ref_d.percentage==percentage].iat[0,1])

tidy_data["d"] = d

tidy_data.to_csv("aggregated_data.txt")
#tidy_data.to_excel("aggregated_data.xlsx")


#%% build the mean data frame just in case

data = pd.read_csv("aggregated_data.txt")

data = data.groupby(["modulation_type", "ISI"])
data = pd.DataFrame(dict(percentage_correct= data.percentage_correct.apply(np.mean), 
                     percent_sd = data.percentage_correct.apply(np.std), d = data.d.apply(np.mean), 
                     d_sd = data.d.apply(np.std)))

data.to_csv("mean_data.txt")
#data.to_excel("mean_data.xlsx")

