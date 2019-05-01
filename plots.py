# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 19:46:00 2019

@author: Antoine
"""

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
    return data

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
ind = plot_individuel(data, subject)

plot_moyen(data)