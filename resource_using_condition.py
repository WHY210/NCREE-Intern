import sqlite3

path = "D:\\NCREE\\DESsimulation"  
dbfile = "Tri1000Treat1000BED100_Pratio_Pratio"
con = sqlite3.connect("%s\\output\\all_%s_MonitorTriTreat_301010\\Queue_079g_TriTLO_8.sqlite" %(path, dbfile))
cur = con.cursor()

def create_table_Resource_check(cur):
    cur.execute("DROP TABLE IF EXISTS Resource_check")
    cur.execute("""
                CREATE TABLE Resource_check
                (Hospital, Run_ID, nDay_6hr, using_tri, using_treat)
                """)           
con.commit()
create_table_Resource_check(cur)

for hospital in range(8):

    # normal rescource
    normal = []
    cur.execute("""
                SELECT max(available_triage), max(available_treatment)
                FROM Resource_Records_079g_300
                WHERE Hospital = %s AND Time = 0 
                """ %(hospital))
    for row in cur.fetchall(): normal = [row[0],row[1]]
    print("hospital %s normal = %s" %(hospital,normal))

    # count using resource (unit:6hr)
    for Run_ID in range(1, 300+1):
        Time, release_additional_triage, available_triage,release_additional_treatment, available_treatment = [],[],[],[],[]
        cur.execute("""SELECT Time, release_additional_triage,    available_triage, 
                                    release_additional_treatment, available_treatment
                        FROM Resource_Records_079g_300
                        WHERE Run_ID = %s AND Hospital = %s""" %(Run_ID, hospital))
        for row in cur.fetchall():
            Time.append(row[0])
            release_additional_triage.append(row[1])
            available_triage.append(row[2])
            release_additional_treatment.append(row[3])
            available_treatment.append(row[4])
        for i in range(len(Time)):
            nDay = Time[i] // (24*60)
            nDay_6hr = ((Time[i] % (24*60)) // (6*60) ) *0.25 + nDay 
            # 0~6hr = nDay.0 / 6~12hr = nDay.25 / 12~18hr = nDay.5 / 18~24hr = nDay.75
            using_tri   = normal[0]   + release_additional_triage[i]    - available_triage[i]
            using_treat = normal[1]   + release_additional_treatment[i] - available_treatment[i]
            cur.execute("""
                        INSERT INTO Resource_check 
                        (Hospital, Run_ID, nDay_6hr, using_tri, using_treat) 
                        VALUES(%s, %s, %s, %s, %s)
                        """ %(hospital, Run_ID, nDay_6hr, using_tri, using_treat))
            con.commit()
        print("complete hospital %s run %s" %(hospital, Run_ID))

# each run / each hospital / per 6hr
cur.execute("""
            CREATE TABLE Resource_using_300_6hr as
            SELECT
                Run_ID, Hospital, nDay_6hr, 
                MAX(using_tri) as max_using_tri,
                MAX(using_treat) as max_using_treat
            FROM Resource_check
            GROUP BY Run_ID, Hospital, nDay_hour 
            """)                         

# 300 run mean / each hospital / per 6hr
cur.execute("""
            CREATE TABLE Resource_using_total as
            SELECT
                Hospital, nDay_6hr, 
                FLOOR(nDay_6hr) as nDay,
                AVG(max_using_tri) as mean_max_using_tri,
                MIN(max_using_tri) as min_max_using_tri,
                MAX(max_using_tri) as max_max_using_tri,
                AVG(max_using_treat) as mean_max_using_treat,
                MIN(max_using_treat) as min_max_using_treat,
                MAX(max_using_treat) as max_max_using_treat,
            FROM Resource_using_300_6hr 
            GROUP BY Hospital, nDay_hour 
            """)

con.commit()
con.close()