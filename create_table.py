import sqlite3
import math

# Sqlite has no Stddev_samp
class StdevFunc:
    def __init__(self):
        self.M = 0.0
        self.S = 0.0
        self.k = 1

    def step(self, value):
        if value is None:
            return
        tM = self.M
        self.M += (value - tM) / self.k
        self.S += (value - tM) * (value - self.M)
        self.k += 1

    def finalize(self):
        if self.k < 3:
            return None
        return math.sqrt(self.S / (self.k-2))


def create_table(path, dbfile):
    con = sqlite3.connect(path + '\\output\\all_%s_MonitorTriTreat_301010\\Queue_079g_TriTLO_8.sqlite' %(dbfile))
    cur = con.cursor() 
    
    # Produce nDay table
    query = '''Create Table Process_Time_079_day as
            SELECT
                Hospital, nDay,
                Count(Distinct(Run_ID)) as Num_run,
                Count(Patient_ID)/Max(Run_ID) as Patient_num,
                AVG(dT) as Avg_dT,
                AVG(t3-t0) as time_before_treatment,
                AVG(t1_t0) as Q_for_Tri,
                AVG(t3_t2) as Q_for_Treatment,
                AVG(t5_t4) as Q_for_Lab,
                AVG(t7_t6) as Q_for_OB2,
                AVG(t7_t4) as Q_for_OB1
            FROM Time_Records_079g_300
            Group by Hospital, nDay'''
    try:
        cur.execute("SELECT EXISTS(SELECT * FROM Process_Time_079_day)")
        if cur.fetchall() == [(1.)]:
            pass
    except: 
        cur.execute(query)

    

    
    # Sqlite has no Stddev_samp
    con.create_aggregate('Stddev_samp', 1, StdevFunc)
    
    # Produce dayNpath table
    query = '''Create Table Process_Time_079_dayNpath as
            SELECT
                Hospital, nDay, Path,
                Count(Distinct(Run_ID)) as Num_run,
                Count(Patient_ID) as Num_patient,
                AVG(dT) as Avg_dT,
                Stddev_samp(dT) as Std_dT,
                AVG(t3-t0) as time_before_treatment,
                AVG(t1_t0) as Q_for_Tri,
                AVG(t3_t2) as Q_for_Treatment,
                AVG(t5_t4) as Q_for_Lab,
                AVG(t7_t6) as Q_for_OB2,
                AVG(t7_t4) as Q_for_OB1
            FROM Time_Records_079g_300
            Group by Hospital, nDay, Path
            Order by nDay'''    
    try:
        cur.execute("SELECT EXISTS(SELECT * FROM Process_Time_079_dayNpath)")
        if cur.fetchall() == [(1.)]:
            pass
    except: 
        cur.execute(query)
    
    
    # Produce dayNtype table
    query = '''Create Table Process_Time_079_dayNtype as
            SELECT
                Hospital, nDay, Type,
                count(Distinct(Run_ID)) as Num_run,
                count(*) as Num_patient,
                AVG(dT) as Avg_dT,
                Stddev_samp(dT) as Std_dT,
                AVG(t3-t0) as time_before_treatment,
                AVG(t1_t0) as Q_for_Tri,
                AVG(t3_t2) as Q_for_Treatment,
                AVG(t5-t4) as Q_for_Lab,
                AVG(t7_t6) as Q_for_OB2,
                AVG(t7_t4) as Q_for_OB1,
                AVG(Wait_for_Operation) as Q_for_OP,
                AVG(Wait_for_Admission) as Q_for_Bed
            FROM Time_Records_079g_300
            Group by Hospital, nDay, Type'''
    try:
        cur.execute("SELECT EXISTS(SELECT * FROM Process_Time_079_dayNtype)")
        if cur.fetchall() == [(1.)]:
            pass
    except: 
        cur.execute(query)
    


    # Produce nDay table
    query = '''Create Table Process_Time_079_avgday as
            SELECT
                Hospital, nDay,
                AVG(Avg_dT) as Avg_dT,
                AVG(time_before_treatment) as time_before_treatment,
                AVG(Q_for_Tri) as Q_for_Tri, 
                AVG(Q_for_Treatment) as Q_for_Treatment, 
                AVG(Q_for_Lab) as Q_for_Lab,
                AVG(Q_for_OB2) as Q_for_OB2,
                AVG(Q_for_OB1) as Q_for_OB1,
                AVG(Q_for_OP) as Q_for_OP,
                AVG(Q_for_Bed) as Q_for_Bed
            FROM Process_Time_079_dayNtype
            Group by Hospital, nDay'''
    try:
        cur.execute("SELECT EXISTS(SELECT * FROM Process_Time_079_avgday)")
        if cur.fetchall() == [(1.)]:
            pass
    except: 
        cur.execute(query)

        
        
    con.commit()
    con.close()
    print("finish creating missing tables")
    return



