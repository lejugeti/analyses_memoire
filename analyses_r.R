library(ez)
library(afex)
data = read.csv("C:/Users/Antoi/Documents/Afc_ExpeMemoire_VersionPC/analyses/aggregated_data.txt")

data$subject = as.factor(data$subject)
data$ISI = as.factor(data$ISI)
str(data)
a = data[data["subject"]==2, c("subject", "ISI", "modulation_type", "percentage_correct")]
b = data[data["subject"]==3, c("subject", "ISI", "modulation_type", "percentage_correct")]
c = rbind(a,b)

lel = ezANOVA(data = c, dv="percentage_correct", within=.("ISI","modulation_type"), wid="subject")

lol = aov_ez(id="subject", dv="percentage_correct", within=c("ISI", "modulation_type"), data=data)
