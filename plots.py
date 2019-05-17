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
        fm.append(data[data.modulation_type == "FM"][data.ISI== time].iat[0, 6])
        am.append(data[data.modulation_type == "AM"][data.ISI== time].iat[0, 6])
    
            
    isi = isi = [500, 500 * np.sqrt(2), 1000, 1000 * np.sqrt(2), 2000]
    plt.plot(isi, fm, "o", color="red", linestyle="none", label="FM")
    plt.plot(isi, am, "o", color="blue", linestyle="none", label="AM")
    
    plt.xscale("log")
    #plt.xticks(isi)
    plt.ylim(0, 1.4)
    plt.legend(loc=0)
    plt.xlabel("ISI (ms)")
    plt.ylabel("d'")
    
    plt.title(f"S{subject}")
    
    if save:
        plt.savefig(f"figures/figure_S{subject}.pdf")
    
    plt.show()



def plot_pilote(data, subject_nb, save=False):
    """
    plot les fonctions d'oubli avec 6 ISI au lieu de 5
    """
    
    data = data[data.subject == subject_nb]
    
    isi = range(1,7)
    fm = []
    am = []
    
    for time in isi:
        #iat[0,5] pour prendre la valeur de percentage correct dans la ligne
        fm.append(data[data.modulation_type == "FM"][data.ISI== time].iat[0, 6])
        am.append(data[data.modulation_type == "AM"][data.ISI== time].iat[0, 6])

            
    isi = isi = [500, 500 * np.sqrt(2), 1000, 1000 * np.sqrt(2), 2000, 4000]
    plt.plot(isi, fm, "o", color="red", linestyle="none", label="FM")
    plt.plot(isi, am, "o", color="blue", linestyle="none", label="AM")
    
    plt.xscale("log")
    #plt.xticks(isi)
    plt.ylim(0, 1.4)
    plt.legend(loc=0)
    plt.xlabel("ISI (ms)")
    plt.ylabel("percentage correct")
    
    plt.title(f"S{subject}")
    if save:
        plt.savefig(f"figures/figure_6_ISI.pdf")
        
        
    plt.show()



def plot_modulation(data, sujets, modulation=None, save=False):
    """plot les fonctions d'oubli de tous les sujets pour un type de modulation"""
    
    isi = [500, 500*np.sqrt(2), 1000, 1000*np.sqrt(2), 2000]
    data = data[data.modulation_type==modulation]
    
    for sub in sujets:
        temp = data[data.subject == sub]
        temp = temp[temp.ISI<6]
        plt.plot(isi, temp.d, 
                 label= f"{sub}")
    
    plt.xscale("log")
    plt.xlabel("ISI (ms)")
    plt.ylabel("d'")
    plt.ylim(0, 1.4)
    #plt.legend(loc=0)
    plt.title(f"Fonctions d'oubli individuelles pour {modulation}")
    if save:
        plt.savefig(f"figures/figure_{modulation}.pdf")
    plt.show()


def plot_moyen(data, save=False):
    """
    plot les fonctions d'oubli moyennées pour AM et FM
    """
    #pour avoir le dataframe sans le 6e isi
    data = data[data.ISI<6]
    
    #valeurs à plot
    isi = [500, 500*np.sqrt(2), 1000, 1000*np.sqrt(2), 2000]
    am = data[data.modulation_type=="AM"]["percentage_correct"]
    fm = data[data.modulation_type=="FM"]["percentage_correct"]
    am_error = data[data.modulation_type=="AM"]["percent_sd"]
    fm_error = data[data.modulation_type=="FM"]["percent_sd"]
    
    
    plt.errorbar(isi, fm, yerr=fm_error, marker="o", color="red", alpha=0.5, label="FM")
    plt.errorbar(isi, am, yerr=am_error, marker="o", color="blue", alpha=0.5, label="AM")
    
    plt.xscale("log")
    plt.ylim(0, 100)
    plt.legend(loc=0)
    plt.xlabel("ISI (ms)")
    plt.ylabel("percentage correct (%)")
    plt.title("averaged function")
    plt.yticks(range(0,101, 10))
    if save:
        plt.savefig("figures/figure_moyenne.pdf")
    plt.show()

def plot_moyen_d(data, save=False):
    """
    plot les fonctions d'oubli moyennées pour AM et FM
    """
    #pour avoir le dataframe sans le 6e isi
    data = data[data.ISI<6]
    
    #valeurs à plot
    isi = [500, 500*np.sqrt(2), 1000, 1000*np.sqrt(2), 2000]
    am = data[data.modulation_type=="AM"]["d"]
    fm = data[data.modulation_type=="FM"]["d"]
    am_error = data[data.modulation_type=="AM"]["d_sd"]
    fm_error = data[data.modulation_type=="FM"]["d_sd"]
    
    
    plt.errorbar(isi, fm, yerr=fm_error, marker="o", color="red", alpha=0.7, label="FM")
    plt.errorbar(isi, am, yerr=am_error, marker="o", color="blue", alpha=0.7, label="AM")
    
    plt.xscale("log")
    plt.ylim(0, 1.4)
    plt.legend(loc=0)
    plt.xlabel("ISI (ms)")
    plt.ylabel("d'")
    plt.title("averaged function")
    #plt.yticks(range(0,101, 10))
    if save:
        plt.savefig("figures/figure_moyenne_d.pdf")
    plt.show()


data = pd.read_csv("aggregated_data.txt")
data["subject"] = data["subject"].astype("category")
data["modulation_type"] = data["modulation_type"].astype("category")
#data["ISI"] = data["ISI"].astype("category")

#%%plot individuel
subject = 8
ind = plot_individuel(data, subject, save=True)

#%% plot 6 ISI
subject = 10
plot_pilote(data, subject, save=True)
#%% plot avec données moyennées
mean_data = pd.read_csv("mean_data.txt")
plot_moyen(mean_data, save=True)

plot_moyen_d(mean_data, save=True)

#%% plot individuels AM et FM

subjects = [1,2,3,5,6,7,8,9]

plot_modulation(data, subjects, modulation="AM", save=True)
plot_modulation(data, subjects, modulation="FM", save=True)