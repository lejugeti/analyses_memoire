# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 08:26:31 2019

@author: Antoine
"""
#%% cleaning the matlab data
import pandas as pd
import os
#a = pd.read_excel("Discrimination2_CS_AM_and_FM_ISI2_S1.dat")
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

#%% plot des fonctions d'oubli 
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_individuel(data, subject_nb):
    """
    Permet de plot les fonctions d'oubli individuelles d'un sujet pour AM et FM
    """
    
    data = data[data.subject == subject_nb]
    
    isi = range(1,6)
    fm = []
    am = []
    for time in isi:
        #iat[0,5] pour prendre la valeur de percentage correct dans la ligne
        fm.append(data[data.modulation_type == "FM"][data.ISI==time].iat[0, 5])
        am.append(data[data.modulation_type == "AM"][data.ISI==time].iat[0, 5])
    
    plt.plot(isi, fm, "o", color="red", linestyle="none", label="FM")
    plt.plot(isi, am, "o", color="blue", linestyle="none", label="AM")
    plt.xticks(isi)
    plt.ylim(0, 100)
    plt.legend(loc=0)
    plt.xlabel("ISI (condition)")
    plt.ylabel("percentage correct")
    plt.title(f"S{subject}")
    #plt.savefig(f"figures/figure_S{subject}.pdf")
    plt.show()

def plot_moyen(data):
    """
    plot les fonctions d'oubli moyennées pour AM et FM
    """
    
    grouped = data.groupby(["modulation_type", "ISI"])
    grouped_mean = grouped["percentage_correct"].apply(np.mean)
    
    #valeurs à plot
    isi = range(1,6)
    am = list(grouped_mean[:5])
    fm = list(grouped_mean[5:])
    
    plt.plot(isi, fm, "o", color="red", linestyle="none", label="FM")
    plt.plot(isi, am, "o", color="blue", linestyle="none", label="AM")
    plt.xticks(isi)
    plt.ylim(0, 100)
    plt.legend(loc=0)
    plt.xlabel("ISI (condition)")
    plt.ylabel("percentage correct")
    plt.title("averaged function")
    #plt.savefig("figures/figure_moyenne.pdf")
    plt.show()
    
data = pd.read_csv("aggregated_data.txt")
subject = 2
plot_individuel(data, subject)

plot_moyen(data)




