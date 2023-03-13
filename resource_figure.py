import sqlite3
import matplotlib.pyplot as plt
import os

def subfigure(path, dbfile, x, y):
    plt.figure(figsize=(8,4), dpi = 500)
    for hospital in range(8):
        plt.subplot(int("24" + str(hospital+1)))
        plt.title("hospital" + str(hospital), fontsize=5)
        plt.plot(x[0][hospital], y[0][hospital], linewidth=0.75)
        plt.xlim(0,x[1])
        plt.ylim(0,y[1])
        plt.xlabel(x[2], fontsize=5)
        plt.ylabel(y[2], fontsize=5)
        plt.xticks(fontsize=5)
        plt.yticks(fontsize=5)
        plt.text(x=46*x[3], y=y[3][hospital]+y[4], s="%3f" %(y[3][hospital]), fontsize=5)
        plt.axvspan(46*x[3], 49*x[3], color='r', alpha=0.1)
    plt.tight_layout()
    plt.suptitle(x[2] + "-" + y[2], fontsize=5)
    plt.savefig("%s\\output\\figure\\resource\\%s\\%s_%s.png" %(path, dbfile, x[2], y[2]))
    return

def rescource_figure(path,dbfile):

    con = sqlite3.connect("%s\\output\\all_%s_MonitorTriTreat_301010\\Queue_079g_TriTLO_8.sqlite" %(path, dbfile))
    cur = con.cursor()

    nDay,Sixhr,tri,treat = [[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[]], [[],[],[],[],[],[],[],[]]
    max_tri, max_treat = [], []
    for hospital in range(8):
        cur.execute("""
                    SELECT 
                    nDay, Sixhr, avg_max_using_tri, avg_max_using_treat
                    FROM Resource_using
                    WHERE Hospital = %s
                    """%(hospital))
        for row in cur.fetchall():
            nDay[hospital].append(row[0])
            Sixhr[hospital].append(row[1])
            tri[hospital].append(row[2])
            treat[hospital].append(row[3])
        max_tri.append(max(tri[hospital]))
        max_treat.append(max(treat[hospital]))

    x_nDay  = [nDay,  60,   "nDay", 1]
    x_hr    = [Sixhr, 1440, "hr", 24]
    y_tri   = [tri,   5,    "triage",  max_tri, 0.1]
    y_treat = [treat, 45,   "treatment",  max_treat, 1]

    if(os.path.exists(path + "\\output\\figure") == False): os.mkdir(path + "\\output\\figure")
    if(os.path.exists(path + "\\output\\figure\\resource") == False): os.mkdir(path + "\\output\\figure\\resource")
    if(os.path.exists(path + "\\output\\figure\\resource\\" + dbfile) == False): os.mkdir(path + "\\output\\figure\\resource\\" + dbfile)

    subfigure(path, dbfile, x_nDay, y_tri)
    subfigure(path, dbfile, x_hr,   y_tri)
    subfigure(path, dbfile, x_nDay, y_treat)
    subfigure(path, dbfile, x_hr,   y_treat)

    return