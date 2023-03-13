import sqlite3

def resource(path, dbfile):
    con = sqlite3.connect("%s\\output\\all_%s_MonitorTriTreat_301010\\Queue_079g_TriTLO_8.sqlite" %(path, dbfile))
    cur = con.cursor()

    # count using_rescource (unit:Time(min)/each run)
    cur.execute("DROP TABLE IF EXISTS Resource_using_Time")
    cur.execute("""
                CREATE TABLE Resource_using_Time(
                Run_ID, Hospital, Time, using_tri, using_treat)
                """)
    
    for hospital in range(8):

        # normal resource number
        cur.execute("""
                SELECT max(available_triage), max(available_treatment)
                FROM Resource_Records_079g_300
                WHERE Hospital = %s AND Time = 0 
                """%(hospital))   
        for row in cur.fetchall(): normal = [row[0],row[1]]
        print("hospital %s normal = %s" %(hospital,normal))
    
        cur.execute("""
                    INSERT INTO Resource_using_Time 
                    SELECT 
                        Run_ID, Hospital , Time,
                        %s + release_additional_triage - available_triage,  
                        %s + release_additional_treatment - available_treatment
                    FROM Resource_Records_079g_300
                    WHERE Hospital = %s
                    ORDER BY Hospital, Run_ID, Time
                    """%(normal[0], normal[1], hospital))
        con.commit()

    # max_using_resouce (unit:6hr/each run)
    cur.execute("DROP TABLE IF EXISTS Resource_using_300")
    cur.execute("""
                CREATE TABLE Resource_using_300 AS     
                SELECT 
                    Run_ID, Hospital, 
                    FLOOR(Time/1440) + 1 as nDay,
                    FLOOR(Time/360) * 6 as Sixhr,
                    MAX(using_tri) as max_using_tri, 
                    MAX(using_treat) as max_using_treat
                FROM Resource_using_Time
                GROUP BY Hospital, Run_ID, FLOOR(Time/360)
                ORDER BY Hospital, Run_ID, Sixhr
                """)
    con.commit()

    # 300runAVG_max_using_resouce (unit:6hr)
    cur.execute("DROP TABLE IF EXISTS Resource_using")
    cur.execute("""
                CREATE TABLE Resource_using AS
                SELECT 
                    Hospital, nDay, Sixhr,
                    AVG(max_using_tri)       as avg_max_using_tri,
                    AVG(max_using_treat)     as avg_max_using_treat,
                    MIN(max_using_tri)       as min_max_using_tri,
                    MAX(max_using_tri)       as max_max_using_tri,
                    MIN(max_using_treat)     as min_max_using_treat,
                    MAX(max_using_treat)     as max_max_using_treat
                FROM Resource_using_300
                GROUP BY Hospital, Sixhr
                ORDER BY Hospital, Sixhr
                """)    
    con.commit()
    con.close()