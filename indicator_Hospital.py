import sqlite3

def indicator_Hospital(path, dbfile):
    con = sqlite3.connect(path + "\\output\\all_" + dbfile + "_MonitorTriTreat_301010\\Queue_079g_TriTLO_8.sqlite")
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS indicator_Hospital")
    cur.execute("CREATE TABLE indicator_Hospital(Hospital, nDay, Type, time_before_treatment, Q_for_OP, Q_for_Bed)")
    time = [5, 10, 30, 60, 120]
    for Hospital in range(8):
        for Type in range(5):
            cur.execute("SELECT Hospital, nDay, Type, time_before_treatment, Q_for_OP, Q_for_Bed \
                         FROM Process_Time_079_dayNtype \
                         WHERE Hospital = %s AND Type =%s AND nDay >= 43 AND nDay <= 54" %(Hospital, Type))
            for row in cur.fetchall(): 
                if row[4] == None and row[5] == None:
                    cur.execute("INSERT INTO indicator_Hospital VALUES(%s,%s,%s,%s,%s,%s) \
                                " %(row[0], row[1], row[2], row[3]/time[Type], "NULL", "NULL"))
                elif row[4] == None:
                    cur.execute("INSERT INTO indicator_Hospital VALUES(%s,%s,%s,%s,%s,%s) \
                                " %(row[0], row[1], row[2], row[3]/time[Type], "NULL", row[5]/480))
                elif row[5] == None:
                    cur.execute("INSERT INTO indicator_Hospital VALUES(%s,%s,%s,%s,%s,%s) \
                                " %(row[0], row[1], row[2], row[3]/time[Type], row[4]/30, "NULL"))
                else:
                    cur.execute("INSERT INTO indicator_Hospital VALUES(%s,%s,%s,%s,%s,%s) \
                                " %(row[0], row[1], row[2], row[3]/time[Type], row[4]/30, row[5]/480))    
    con.commit()
    con.close()

