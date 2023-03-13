import sqlite3
import matplotlib.pyplot as plt
import os

def figure(cur, place, Type, name, wait, y):
    Day = []
    cur.execute("SELECT nDay FROM indicator_Hospital WHERE Type = 0 AND Hospital = 0 AND nDay >= 43 AND nDay <= 54")
    for row in cur.fetchall(): Day.append(row[0])
    wait_lst = []
    for Hospital in range(8):
        Hospital_lst = []
        for nDay in range(43,54+1):
            cur.execute("SELECT %s FROM indicator_Hospital \
                        WHERE Type = %s AND nDay = %s AND Hospital = %s" %(wait, Type, nDay, Hospital))
            for row in cur.fetchall():
                Hospital_lst.append(row[0])
        wait_lst.append(Hospital_lst)
    plt.subplot(place)    
    for item in wait_lst: 
        plt.plot(Day, item,linewidth = '0.75')
    plt.axvspan(46, 49, color='r', alpha=0.1)
    plt.rc('legend', fontsize=4)
    plt.xlabel("nDay", fontsize=4)
    plt.xticks(range(43, 55), fontsize=4) 
    plt.yticks(fontsize=4)
    plt.ylim(0,y)
    plt.title(name + "\n" + wait, fontsize=4)
    plt.grid(True, linestyle = "--",color = 'gray' ,linewidth = '0.5',axis='both', alpha=0.5)
    return

def TotalFigure(path, name, wait, y):
    con = sqlite3.connect(path + "\\output\\all_" + name + "_MonitorTriTreat_301010\\Queue_079g_TriTLO_8.sqlite")
    cur = con.cursor()
    plt.figure(figsize=(6, 4), dpi=2000)     
    figure(cur, 231, 0, name + "\n Type0", wait, y)
    figure(cur, 232, 1, name + "\n Type1", wait, y)
    figure(cur, 233, 2, name + "\n Type2", wait, y)
    figure(cur, 234, 3, name + "\n Type3", wait, y)
    figure(cur, 235, 4, name + "\n Type4", wait, y)
    wait_lst = [[None], [None], [None], [None], [None], [None], [None], [None]]
    Day = [0]
    plt.subplot(236) 
    for item in wait_lst:  plt.plot(Day, item)
    plt.legend(['Hospital0','Hospital1', 'Hospital2', 'Hospital3', 'Hospital4', 'Hospital5', 'Hospital6', 'Hospital7'], frameon = False, fontsize=5, loc=10)
    plt.xticks(alpha=0)
    plt.yticks(alpha=0)
    plt.tight_layout()
    plt.savefig(path + "\\output\\figure\\Hospital\\" + wait + "\\" + name + "_" + wait + ".png")
    con.commit()
    con.close()
    return

def AllTotalFigure(path, dbfile):
    if(os.path.exists(path + "\\output\\figure\\Hospital") == False): os.mkdir(path + "\\output\\figure\\Hospital")
    if(os.path.exists(path + "\\output\\figure\\Hospital\\time_before_treatment") == False): os.mkdir(path + "\\output\\figure\\Hospital\\time_before_treatment")
    if(os.path.exists(path + "\\output\\figure\\Hospital\\Q_for_OP") == False): os.mkdir(path + "\\output\\figure\\Hospital\\Q_for_OP")
    if(os.path.exists(path + "\\output\\figure\\Hospital\\Q_for_Bed") == False): os.mkdir(path + "\\output\\figure\\Hospital\\Q_for_Bed")
    TotalFigure(path, dbfile, "time_before_treatment", 5)
    TotalFigure(path, dbfile, "Q_for_OP",16)
    TotalFigure(path, dbfile, "Q_for_Bed",16.5)
    return