% Résultats pilote Antoine
Sub={'S2'};
path='./Results/';
Reps=5;
modType={'AM','FM'}
modRates=3;
probs=0.76;


for modType={'AM'}
% ISI1=500 ms; ISI2 = 707.1 ms; ISI3= 1s ; ISI4= 1.41 s    ; ISI5= 2 s
ISI1=read_ConstantStimuli_ISI1(Sub,path,Reps,modType,modRates,probs);
ISI1_AM=sum(ISI1)/(length(ISI1)*20);

ISI2=read_ConstantStimuli_ISI2(Sub,path,Reps,modType,modRates,probs);
ISI2_AM=sum(ISI2)/(length(ISI2)*20);

ISI3=read_ConstantStimuli_ISI3(Sub,path,Reps,modType,modRates,probs);
ISI3_AM=sum(ISI3)/(length(ISI3)*20);

ISI4=read_ConstantStimuli_ISI4(Sub,path,Reps,modType,modRates,probs);
ISI4_AM=sum(ISI4)/(length(ISI4)*20);

ISI5=read_ConstantStimuli_ISI5(Sub,path,Reps,modType,modRates,probs);
ISI5_AM=sum(ISI5)/(length(ISI5)*20);

% AVEC ROVING
AM_Detection_THRESHOLD=nanmean(read_Adaptive_AM_and_FM(Sub,path,Reps,modType,modRates,probs))
AM_Discrimination_THRESHOLD=nanmean(read_Discrimination1_AM_and_FM(Sub,path,Reps,modType,modRates,probs))

% SANS ROVING
AM_Detection_THRESHOLD_NR=nanmean(read_AdaptiveB_AM_and_FM_NR(Sub,path,Reps,modType,modRates,probs))
AM_Discrimination_THRESHOLD_NR=nanmean(read_Discrimination1B_AM_and_FM_NR(Sub,path,Reps,modType,modRates,probs))


end

for modType={'FM'}
% ISI1=500 ms; ISI2 = 707.1 ms; ISI3= 1s ; ISI4= 1.41 s    ; ISI5= 2 s
ISI1=read_ConstantStimuli_ISI1(Sub,path,Reps,modType,modRates,probs);
ISI1_FM=sum(ISI1)/(length(ISI1)*20);

ISI2=read_ConstantStimuli_ISI2(Sub,path,Reps,modType,modRates,probs);
ISI2_FM=sum(ISI2)/(length(ISI2)*20);

ISI3=read_ConstantStimuli_ISI3(Sub,path,Reps,modType,modRates,probs);
ISI3_FM=sum(ISI3)/(length(ISI3)*20);

ISI4=read_ConstantStimuli_ISI4(Sub,path,Reps,modType,modRates,probs);
ISI4_FM=sum(ISI4)/(length(ISI4)*20);

ISI5=read_ConstantStimuli_ISI5(Sub,path,Reps,modType,modRates,probs);
ISI5_FM=sum(ISI5)/(length(ISI5)*20);

% AVEC ROVING
FM_Detection_THRESHOLD=nanmean(read_Adaptive_AM_and_FM(Sub,path,Reps,modType,modRates,probs))
FM_Discrimination_THRESHOLD=nanmean(read_Discrimination1_AM_and_FM(Sub,path,Reps,modType,modRates,probs))

% SANS ROVING
FM_Detection_THRESHOLD_NR=nanmean(read_AdaptiveB_AM_and_FM_NR(Sub,path,Reps,modType,modRates,probs))
FM_Discrimination_THRESHOLD_NR=nanmean(read_Discrimination1B_AM_and_FM_NR(Sub,path,Reps,modType,modRates,probs))
end




x=[0.5 0.7071 1 1.41 2];
y_AM=[ISI1_AM ISI2_AM ISI3_AM ISI4_AM ISI5_AM];
y_FM=[ISI1_FM ISI2_FM ISI3_FM ISI4_FM ISI5_FM];
figure;plot(x,y_AM,'s');
hold on;
plot(x,y_FM,'sr');
legend({'AM','FM'},'Location','southwest')
set(gca,'xlim',[0 3],'ylim',[0 1]);
title('Roving condition','fontsize',16);
xlabel('ISI (ms)','fontsize',14);
ylabel('Percent Correct (%)','Fontsize',14);


