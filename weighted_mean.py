import sqlite3

# create table "Region_waiting_time"
def create_table_Region_waiting_time(cur):
    cur.execute("DROP TABLE IF EXISTS Region_waiting_time")
    cur.execute("CREATE TABLE Region_waiting_time(nDay INTEGER, Type INTEGER, \
                 time_before_treatment INTEGER, Q_for_OP INTEGER, Q_for_Bed INTEGER)")
    
# create table "Patient_distribution_hospital" (for checking)
def create_table_Patient_distribution_hospital(cur):
    cur.execute("DROP TABLE IF EXISTS Patient_distribution_hospital")
    cur.execute("CREATE TABLE Patient_distribution_hospital(Hospital INTEGER, nDay INTEGER, Type INTEGER, \
                 Treatment_count INTEGER, Treatment_percentage INTEGER, \
                 OP_count INTEGER, OP_percentage INTEGER, \
                 Bed_count, Bed_percentage)")

# create own lists for each ([Hospital 0, 1, 2, 3...7], float or "NULL")
def create_list (d, t, h, cur, nDay, Type, Name, lst_of_it):
    for Hospital in range(h):
        cur.execute("SELECT %s FROM Process_Time_079_dayNtype WHERE Type = %d AND nDay = %d AND Hospital = %d \
                     ORDER BY ROWID" %(Name, Type, nDay, Hospital))
        for row in cur.fetchall(): 
            if row[0] == None: lst_of_it.append("NULL")
            else: lst_of_it.append(row[0])
    return lst_of_it

# patient count/percentage of each hospital ( = Treatment)
def patient(d, t, h, cur, nDay, Type, Num_patient):
    Num_patient = create_list(d, t, h, cur, nDay, Type, "Num_patient", Num_patient)
    Sum_patient, result = 0, [Num_patient,[]]  # result = [Num_patient, Percentage]
    for Hospital in range(h): Sum_patient += Num_patient[Hospital]
    for Hospital in range(h): result[1].append(Num_patient[Hospital]/Sum_patient)
    return result

# patient count/percentage of each hospital only within operation patients (OP = Type0)
def patient_OP(d, t, h, cur, nDay, Type, Num_patient): 
    result = [[],[]]  # result = [Num_OPpatient, Percentage]
    if Type == 0: result = patient(d, t, h, cur, nDay, Type, Num_patient)  # all Type0 undergoes OP and needs Bed (=treatment)
    else:
        for Hospital in range(h):
            result[0].append("NULL")
            result[1].append("NULL")
    return result

# patient count/percentage of each hospital only within admission patients (Bed)
def patient_Bed(d, t, h, cur, nDay, Type, Num_patient): 
    Sum_Bed, result = 0, [[],[]]  # result = [Num_Bedpatient, Percentage]
    if Type == 0: result = patient(d, t, h, cur, nDay, Type, Num_patient)  # all Type0 undergoes OP and needs Bed (=treatment)
    else:
        for Hospital in range(h):
            cur.execute("SELECT COUNT(wait_for_Admission) FROM Time_Records_079g_300 \
                        WHERE nDay = %d AND Type = %d AND Hospital = %d" %(nDay, Type, Hospital))
            for row in cur.fetchall(): 
                result[0].append(row[0])
                Sum_Bed += row[0]
        for Hospital in range(h): result[1].append(result[0][Hospital]/Sum_Bed)
    return result

# compute weighted mean
def mean(d, t, h, cur, nDay, Type, name, lst_of_it, result):
    lst_of_it = create_list(d, t, h, cur, nDay, Type, name, lst_of_it)
    if lst_of_it == ["NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL","NULL"]: MEAN = "NULL"
    else: 
        MEAN = 0
        for Hospital in range(h): 
            if lst_of_it[Hospital] != "NULL": 
                MEAN += lst_of_it[Hospital]*result[1][Hospital]
    return MEAN

def run(d, t, h, con, cur, nDay, Type, Num_patient, time_before_treatment, Q_for_OP, Q_for_Bed):
    Treatment, OP, Bed = patient(d, t, h, cur, nDay, Type, Num_patient), patient_OP(d, t, h, cur, nDay, Type, Num_patient), patient_Bed(d, t, h, cur, nDay, Type, Num_patient)
    
    # write result into "Patient_distribution_hospital"
    for Hospital in range(h):
        cur.execute("INSERT INTO Patient_distribution_hospital VALUES(%d, %d, %d, %s, %s, %s, %s, %s, %s)" \
                    %(Hospital, nDay, Type, Treatment[0][Hospital], Treatment[1][Hospital], \
                                            OP[0][Hospital], OP[1][Hospital], \
                                            Bed[0][Hospital], Bed[1][Hospital]))
    
    # write result into "Region_waiting_time"
    mean_treatment = mean(d, t, h, cur, nDay, Type, "time_before_treatment", time_before_treatment, Treatment)
    mean_OP = mean(d, t, h, cur, nDay, Type, "Q_for_OP", Q_for_OP, OP)
    mean_Bed = mean(d, t, h, cur, nDay, Type, "Q_for_Bed", Q_for_Bed, Bed)
    cur.execute("INSERT INTO Region_waiting_time VALUES(%d, %d, %s, %s, %s)" %(nDay, Type, mean_treatment, mean_OP, mean_Bed))
    con.commit()    
    print("complete nDay = %d Type = %d" %(nDay,Type))
    return
    
def weighted_mean(path, dbfile, d, t, h):
    con = sqlite3.connect(path + '\\output\\all_%s_MonitorTriTreat_301010\\Queue_079g_TriTLO_8.sqlite' %(dbfile))
    cur = con.cursor()
    create_table_Region_waiting_time(cur)
    create_table_Patient_distribution_hospital(cur)
    for nDay in range(1,d+1):
        for Type in range(t):
            Num_patient, time_before_treatment, Q_for_OP, Q_for_Bed = [], [], [], []  
            run(d, t, h, con, cur, nDay, Type, Num_patient, time_before_treatment, Q_for_OP, Q_for_Bed)   
    con.close()
    print("finish weighted_mean")
    return