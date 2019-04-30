# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 08:26:31 2019

@author: Antoine
"""
#%% cleaning the matlab data
import pandas as pd
import os

raw_path = os.path.join("Results", "raw")

for filename in os.listdir(raw_path):
    with open(os.path.join(raw_path, filename)) as file:
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
    
    clean_data["ISI"] = [filename[-8] for i in range(len(clean_data))]
    clean_data = clean_data[["modulation_type", "ISI", "nb_presentation", "nb_correct"]]
    clean_data.index.name = "index"
    clean_data.to_csv(os.path.join('Results', 'clean', f"ISI{filename[-8]}_S{filename[-5]}.txt"))

#%% building the aggregated dataframe thanks to the cleaned files
clean_path = os.path.join("Results", "clean")

clean_agg = pd.DataFrame()
for filename in os.listdir(clean_path):
    data = pd.read_csv(os.path.join(clean_path, filename), index_col="index")
    data["subject"] = [filename[-5] for i in range(len(data))]
    clean_agg = pd.concat([clean_agg, data], ignore_index=True)

clean_agg[["modulation_type", "subject", "ISI"]] = clean_agg[["modulation_type", "subject", "ISI"]].astype("category")

#build new dataframe with sumed correct for each subject MT and ISI
sum_presented = clean_agg.groupby(["subject", "modulation_type",  "ISI"])["nb_presentation"].apply(sum)
sum_correct = clean_agg.groupby(["subject", "modulation_type", "ISI"])["nb_correct"].apply(sum)

tidy_data = pd.DataFrame({"presented":sum_presented, "correct":sum_correct})

#colonne du percentage correct
tidy_data["percentage_correct"] = 100 * tidy_data.correct / tidy_data.presented

tidy_data.to_csv("aggregated_data.txt")






