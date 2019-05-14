# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 19:46:00 2019

@author: Antoine
"""

#%% initialisation des plots 

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def random_color():
    return np.random.random(), np.random.random(), np.random.random()

def plot_individuel(data, subject_nb, save=False):
    """
    Permet de plot les fonctions d'oubli individuelles d'un sujet pour AM et FM
    """
    
    data = data[data.subject == subject_nb]
    
    isi = range(1,6)
    fm = []
    am = []
    for time in isi:
        #iat[0,5] pour prendre la valeur de percentage correct dans la ligne
        fm.append(data[data.modulation_type == "FM"][data.ISI== time].iat[0, 5])
        am.append(data[data.modulation_type == "AM"][data.ISI== time].iat[0, 5])
    
    isi = isi = [500, 500*np.sqrt(2), 1000, 1000*np.sqrt(2), 2000]
    plt.plot(isi, fm, "o", color="red", linestyle="none", label="FM")
    plt.plot(isi, am, "o", color="blue", linestyle="none", label="AM")
    
    plt.xscale("log")
    #plt.xticks(isi)
    plt.ylim(0, 100)
    plt.legend(loc=0)
    plt.yticks(range(0,101, 10))
    plt.xlabel("ISI (ms)")
    plt.ylabel("percentage correct")
    
    plt.title(f"S{subject}")
    if save:
        plt.savefig(f"figures/figure_S{subject}.pdf")
    plt.show()
    return data


def plot_modulation(data, sujets, modulation=None, save=False):
    """plot les fonctions d'oubli de tous les sujets pour un type de modulation"""
    
    isi = [500, 500*np.sqrt(2), 1000, 1000*np.sqrt(2), 2000]
    data = data[data.modulation_type==modulation]
    
    for sub in sujets:
        temp = data[data.subject == sub]
        plt.plot(isi, temp.percentage_correct, color=random_color(), 
                 label= f"{sub}")
    
    plt.xscale("log")
    #plt.xticks(isi)
    plt.yticks([i for i in range(0,101,10)])
    plt.xlabel("ISI (ms)")
    plt.ylabel("percentage correct (%)")
    plt.legend(loc=0)
    plt.title(f"Fonctions d'oubli individuelles pour {modulation}")
    if save:
        plt.savefig(f"figures/figure_{modulation}.pdf")
    plt.show()


def plot_moyen(data, save=False):
    """
    plot les fonctions d'oubli moyennées pour AM et FM
    """
   
    #valeurs à plot
    isi = [500, 500*np.sqrt(2), 1000, 1000*np.sqrt(2), 2000]
    am = data[data.modulation_type=="AM"]["percentage_correct"]
    fm = data[data.modulation_type=="FM"]["percentage_correct"]
    am_error = data[data.modulation_type=="AM"]["ecart_type"]
    fm_error = data[data.modulation_type=="FM"]["ecart_type"]
    
    
    plt.errorbar(isi, fm, yerr=fm_error, marker="o", color="red", alpha=0.5)
    plt.errorbar(isi, am, yerr=am_error, marker="o", color="blue", alpha=0.5)
    
    plt.xscale("log")
    #plt.xticks(isi)
    plt.ylim(0, 100)
    plt.legend(loc=0)
    plt.xlabel("ISI (ms)")
    plt.ylabel("percentage correct (%)")
    plt.title("averaged function")
    plt.yticks(range(0,101, 10))
    if save:
        plt.savefig("figures/figure_moyenne.pdf")
    plt.show()
    
data = pd.read_csv("aggregated_data.txt")
data["subject"] = data["subject"].astype("category")
data["modulation_type"] = data["modulation_type"].astype("category")
data["ISI"] = data["ISI"].astype("category")

#%%plot individuel
subject = 9
ind = plot_individuel(data, subject, save=True)

#%% plot avec données moyennées
mean_data = pd.read_csv("mean_data.txt")
plot_moyen(mean_data, save=True)

#%% plot individuels AM et FM

subjects = [1,2,3,5,6,7,9]

plot_modulation(data, subjects, modulation="AM", save=True)
plot_modulation(data, subjects, modulation="FM", save=True)