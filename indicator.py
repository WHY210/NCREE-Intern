import sqlite3


def create_indicator(cur):
    cur.execute("DROP TABLE IF EXISTS indicator")
    cur.execute("CREATE TABLE indicator(nDay, \
                time_before_treatment_Type0, time_before_treatment_Type1, time_before_treatment_Type2, time_before_treatment_Type3, time_before_treatment_Type4, \
                Q_for_OP_Type0, Q_for_OP_Type1, Q_for_OP_Type2, Q_for_OP_Type3, Q_for_OP_Type4, \
                Q_for_Bed_Type0, Q_for_Bed_Type1, Q_for_Bed_Type2, Q_for_Bed_Type3, Q_for_Bed_Type4)")
    return

def Day(cur):
    Day = []
    cur.execute("SELECT nDay FROM Region_waiting_time WHERE Type = 0 AND nDay >= 43 AND nDay <= 54")
    for row in cur.fetchall(): Day.append(row[0])
    return Day

time = [5, 10, 30, 60, 120]
def treatment_ratio(cur, Type):
    treatment_type = []
    cur.execute("SELECT time_before_treatment FROM Region_waiting_time WHERE Type = %d AND nDay >= 43 AND nDay <= 54" %(Type))
    for row in cur.fetchall(): treatment_type.append(row[0]/time[Type])
    return treatment_type

def OP_ratio(cur, Type):
    OP_type = []
    cur.execute("SELECT Q_for_OP FROM Region_waiting_time WHERE Type = %d AND nDay >= 43 AND nDay <= 54" %(Type))
    for row in cur.fetchall(): 
        if row[0] != None: OP_type.append(row[0]/30)
        else: OP_type.append("NULL")
    return OP_type

def Bed_ratio(cur, Type):
    Bed_type = []
    cur.execute("SELECT Q_for_Bed FROM Region_waiting_time WHERE Type = %d AND nDay >= 43 AND nDay <= 54" %(Type))
    for row in cur.fetchall(): Bed_type.append(row[0]/480)
    return Bed_type
      
def insert(cur):
    for r in range(0, 12):
        cur.execute("INSERT INTO indicator VALUES(%d, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" \
                    %(Day(cur)[r], treatment_ratio(cur, 0)[r], treatment_ratio(cur, 1)[r], treatment_ratio(cur, 2)[r], treatment_ratio(cur, 3)[r], treatment_ratio(cur, 4)[r], \
                      OP_ratio(cur, 0)[r], OP_ratio(cur, 1)[r], OP_ratio(cur, 2)[r], OP_ratio(cur, 3)[r], OP_ratio(cur, 4)[r], \
                      Bed_ratio(cur, 0)[r], Bed_ratio(cur, 1)[r], Bed_ratio(cur, 2)[r], Bed_ratio(cur, 3)[r], Bed_ratio(cur, 4)[r]))
    return

def indicator(path, dbfile):
    con = sqlite3.connect(path + "\\output\\all_" + dbfile + "_MonitorTriTreat_301010\\Queue_079g_TriTLO_8.sqlite")
    cur = con.cursor()
    create_indicator(cur)
    insert(cur)
    con.commit()
    con.close()
    return

