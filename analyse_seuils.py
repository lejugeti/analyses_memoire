# -*- coding: utf-8 -*-
"""
Created on Wed May 22 21:51:27 2019

@author: Antoine
"""

#%%mise en forme
import os 
import pandas as pd
import numpy as np

adapt = pd.read_csv("seuils_adaptatifs.txt", index_col=0)
discr = pd.read_csv("seuils_discrimination.txt", index_col=0)

#adaptatif
group_adapt = adapt.groupby(["subject","modulation_type"])
clean_adapt = pd.DataFrame({"seuils_moyens": group_adapt.seuil.apply(np.mean), "sd_seuils": group_adapt.seuil.apply(np.std)})

clean_adapt.to_csv("mean_adaptive.txt")
#clean_adapt.to_excel("mean_adaptive.xlsx")

#discrimination
group_discr = discr.groupby(["subject","modulation_type"])
clean_discr = pd.DataFrame({"seuils_moyens": group_discr.seuil.apply(np.mean),
                            "sd_seuils": group_discr.seuil.apply(np.std)})

clean_discr.to_csv("mean_discrimination.txt")
#clean_discr.to_excel("mean_discrimination.xlsx")


#%%exploration graphique
import matplotlib.pyplot as plt

path_fig = os.path.join("figures")

data_adapt = pd.read_csv("mean_adaptive.txt")
data_discr = pd.read_csv("mean_discrimination.txt")

subject = [i for i in range(1,1+len(data_adapt.subject.unique()))]

am_adapt = data_adapt[data_adapt.modulation_type=="AM"]["seuils_moyens"]
fm_adapt = data_adapt[data_adapt.modulation_type=="FM"]["seuils_moyens"]

am_discr = data_discr[data_discr.modulation_type=="AM"]["seuils_moyens"]
fm_discr = data_discr[data_discr.modulation_type=="FM"]["seuils_moyens"]
#adaptive am
plt.plot(subject, am_adapt, marker="o",color="blue", label="AM", linestyle="none")
plt.xlabel("sujet")
plt.ylabel("Profondeur de modulation m (%)")
plt.title("AM")
plt.xticks(subject)
plt.savefig(os.path.join(path_fig,"seuils_adaptatifs_am.png"))
plt.show()

#adaptive fm
plt.plot(subject, fm_adapt, marker="o", color="red", label="FM", linestyle="none")
plt.xlabel("sujet")
plt.ylabel("Excursion de fréquence (Hz)")
plt.title("FM")
plt.xticks(subject)
plt.savefig(os.path.join(path_fig,"seuils_adaptatif_fm.png"))
plt.show()

#discrimination
plt.plot(subject, fm_discr, marker="o", color="red", label="FM", linestyle="none")
plt.plot(subject, am_discr, marker="o",color="blue", label="AM", linestyle="none")
plt.xlabel("sujet")
plt.ylabel("différence de cadence de modulation (%)")
plt.xticks(subject)
plt.legend(loc=0)
plt.savefig(os.path.join(path_fig,"seuils_discrimination.png"))
plt.show()


#%% anova des seuils adaptatifs
import pingouin as pg

data_adapt = pd.read_csv("seuils_adaptatifs.txt", index_col=0)
data_discr = pd.read_csv("seuils_discrimination.txt", index_col=0)

adapt_am = data_adapt[data_adapt.modulation_type=="AM"]
adapt_fm = data_adapt[data_adapt.modulation_type=="FM"]

aov_adapt_am = pg.anova(data=adapt_am, dv="seuil", between="subject")
aov_adapt_fm = pg.anova(data=adapt_fm, dv="seuil", between="subject")

pg.print_table(aov_adapt_am)
pg.print_table(aov_adapt_fm)


#%% t-test des seuils de discrimination

discr_t_test = pg.ttest(x=am_discr, y=fm_discr, paired=True, tail="one-sided")
pg.print_table(discr_t_test)

#discr_t_test.to_excel("t_test_seuils_discrimination.xlsx")