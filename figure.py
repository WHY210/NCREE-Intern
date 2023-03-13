# -*- coding: utf-8 -*-

import sqlite3
import matplotlib.pyplot as plt
import os
import indicator

Day = []
for day in range(43, 55): Day.append(day)
    
  
def figure(place, wait, name):
    plt.subplot(place)    
    for item in wait: 
        plt.plot(Day, item, linewidth = '1')
    plt.axvspan(46, 49, color='r', alpha=0.1)
    plt.axvspan(43, 54, ymin=0, ymax=1/6, color='b', alpha=0.05)  #ymax=1/3 # ymax=1/6
    plt.xlabel("nDay", fontsize=5)
    plt.xticks(range(43, 55), fontsize=5) 
    plt.yticks([0,1,2,3,4,5,6], fontsize=5)  # ,4,5,6
    plt.ylim(0,6) #3 # 6
    plt.grid(True, linestyle = "--",color = 'gray' ,linewidth = '0.5',axis='both', alpha=0.5)
    legend=["Type0","Type1","Type2","Type3","Type4"] 
    #plt.legend(legend,fontsize=5,bbox_to_anchor=(1.35, 0.7), loc='right')  ######
    plt.title(name, fontsize=5)   ######
    return

def figure_OP(place, wait, name):
    plt.subplot(place)    
    Color = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    plt.plot(Day, wait[0], color=Color[0], linewidth = '1', label="Type0")
    plt.xlabel("nDay", fontsize=5)
    plt.xticks(range(43, 55), fontsize=5)  
    plt.yticks([0,3,6,9,12,15,18,21,24,27,30], fontsize=5)  # ,9,12,15,18,21,24,27,30
    plt.ylim(0,30) # 6 # 30
    #plt.legend(fontsize=5,bbox_to_anchor=(1.35, 0.875), loc='right')  ######    
    plt.grid(True, linestyle = "--",color = 'gray' ,linewidth = '0.5',axis='both', alpha=0.5)
    ax1=plt.twinx()
    for Type in range(1,5): 
        legend=["Type1","Type2","Type3","Type4"]
        ax1.plot(Day, wait[Type], color=Color[Type-1], linewidth = '1', label=legend[Type-1])
        plt.xticks(range(43, 55), fontsize=5)  
        plt.yticks([0,6], fontsize=5, color='firebrick')
        plt.ylim(0,6)
    plt.axvspan(46, 49, color='r', alpha=0.1)
    plt.axvspan(43, 54, ymin=0, ymax=1/30, color='b', alpha=0.05)   # ymax=1/6 # ymax=1/30
    #plt.legend(fontsize=5,bbox_to_anchor=(1.35, 0.65), loc='right')  ######    
    plt.title(name, fontsize=5)  ######
    return
    
def TotalFigure(path, dbfile):
    plt.figure(figsize=(8,2), dpi=500)   # 直 2.5,6    橫 8,2
    con = sqlite3.connect(path + "\\output\\all_" + dbfile + "_MonitorTriTreat_301010\\Queue_079g_TriTLO_8.sqlite")
    cur = con.cursor()
    treatment = [indicator.treatment_ratio(cur, 0), indicator.treatment_ratio(cur, 1), indicator.treatment_ratio(cur, 2), indicator.treatment_ratio(cur, 3), indicator.treatment_ratio(cur, 4)]
    OP = [indicator.OP_ratio(cur, 0), indicator.OP_ratio(cur, 1), indicator.OP_ratio(cur, 2), indicator.OP_ratio(cur, 3), indicator.OP_ratio(cur, 4)]
    Bed = [indicator.Bed_ratio(cur, 0), indicator.Bed_ratio(cur, 1), indicator.Bed_ratio(cur, 2), indicator.Bed_ratio(cur, 3), indicator.Bed_ratio(cur, 4)]
    figure(131, treatment, dbfile + "\n DTD ") # 直31橫13time_before_treatment
    figure_OP(132, OP, dbfile + "\n ETO ")  #Q_for_OP
    figure(133, Bed, dbfile + "\n HSP ")  #Q_for_Bed
    con.commit()
    con.close()
    plt.tight_layout()
    if(os.path.exists(path + "\\output\\figure") == False): os.mkdir(path + "\\output\\figure")
    if(os.path.exists(path + "\\output\\figure\\new_treatment+OP+Bed") == False): os.mkdir(path + "\\output\\figure\\new_treatment+OP+Bed")
    plt.savefig(path + "\\output\\figure\\new_treatment+OP+Bed\\" + dbfile + ".png")
    return