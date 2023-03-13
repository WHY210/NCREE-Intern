# -*- coding: utf-8 -*-

import sqlite3

def check_patient_num(path, dbfile):
    con = sqlite3.connect(path + '\\output\\all_%s_MonitorTriTreat_301010\\Queue_079g_TriTLO_8.sqlite' %(dbfile))
    cur = con.cursor()
    
    
    
    query = """SELECT nDay, SUM("Treatment_count")
               FROM "Patient_distribution_hospital"
               GROUP BY nDay"""
    cur.execute(query)
    earthquake = []
    for row in cur.fetchall(): 
        if row[0] in range(46,49+1): 
            earthquake.append(int(row[1]))
    else: 
        normal = row[1]
    Sum = earthquake[0]+earthquake[1]+earthquake[2]+earthquake[3]
    print("    (earthquake = %d + %d + %d + %d)" %(earthquake[0], earthquake[1], earthquake[2], earthquake[3]))
    print("-)  (normal =     %d + %d + %d + %d)" %(normal, normal, normal, normal))
    print("----------------------------------------------------------------")
    print("                = %d + %d + %d + %d" %(earthquake[0]-normal, earthquake[1]-normal, earthquake[2]-normal, earthquake[3]-normal))
    print("                =", Sum-normal*4) 
    print("                = 4 *", (Sum-normal*4)/300)
    
    query = """SELECT ROWID, "Hospital", "nDay", "Type", sum("Num_patient")
               FROM "Process_Time_079_dayNtype"
               group by Hospital, nDay"""

    def Sum(lst1, lst2):
        result = lst1[0]-lst2[0]+lst1[1]-lst2[1]+lst1[2]-lst2[2]+lst1[3]-lst2[3]+lst1[4]-lst2[4]
        return result
    print("46-45 : %d + %d + %d + %d + %d = %d" %(day46[0]-day45[0], day46[1]-day45[1], day46[2]-day45[2], day46[3]-day45[3], day46[4]-day45[4], Sum(day46,day45)))


    con.commit()
    con.close()


path = "C:\\Users\\hywu\\Desktop\\DESsimulation"  
dbfile = "Tri2Treat5BED100_Pratio_Pratio"
check_patient_num(path, dbfile)