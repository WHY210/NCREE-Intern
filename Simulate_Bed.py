# cd D:\NCREE\DESsimulation\src
# python main.py -c D:\NCREE\DESsimulation\configs\all_Tri2Treat5BED100_OverP2_OverP2_Repair_MonitorTriTreat_301010.yaml

import sqlite3
import pandas as pd
import csv
import os
import matplotlib.pyplot as plt
import shutil

p = "D:\\NCREE"
while True:
    demo = int(input("Demo = ")) 
    i = demo -1
    bed = str(input("Bed = "))
    name = "Demo%s_%sBed" %(demo, bed)

    #read hospital_ResourceNumber
    hospital_ResourceNumber = pd.read_csv( p + "\\DESsimulation\\hospital_ResourceNumber.csv",encoding='big5')
    Demoxxx = str(hospital_ResourceNumber['h_id'].tolist()[i])
    Days = int(hospital_ResourceNumber['平均住院日'].tolist()[i])

    #read hospital_all醫院人流模擬資源數總表
    hospital_all = pd.read_csv( p + "\\DESsimulation\\hospital_all醫院人流模擬資源數總表.csv")
    Demo_BED = hospital_all.iloc[i].tolist()

    #create new Demoxxx.csv
    Admission = str((Days-2)*24*60) + " " + str((Days+2)*24*60) + " " + str(Days*24*60)  
    hospital_Demoxxx = open( p + '\\DESsimulation\\hospital\\%s.csv' %(Demoxxx), mode='w', newline='')
    writer = csv.writer(hospital_Demoxxx)
    writer.writerow(['','Triage','Treatment','Xray','Observation','Operation','Admission','OccupyResource','Priority'])
    writer.writerow(['AL1+AL2(op)','2.25 0.7','7.5 45 22.5','1.25 9.2','0 7.5 30','120 480 240', Admission,'1 2 1 1 1 1','1'])
    writer.writerow(['AL1+AL2'	  ,'4.5 0.7', '15 90 45',   '2.5 9.2', '0 15 60', '120 480 240', Admission,'1 1 1 1 1 1','2'])
    writer.writerow(['AL3'	      ,'4.5 0.7', '15 90 45',	'2.5 9.2', '0 15 60', '120 480 240', Admission,'1 1 1 1 1 1','3'])
    writer.writerow(['AL4'	      ,'4.5 0.7', '15 90 45',	'2.5 9.2', '0 15 60', '120 480 240', Admission,'1 1 1 1 1 1','3'])
    writer.writerow(['AL5'	      ,'4.5 0.7', '15 90 45',	'2.5 9.2', '0 15 60', '120 480 240', Admission,'1 1 1 1 1 1','3'])
    hospital_Demoxxx.close()

    #create new Demoxxx_xxxBED.csv
    data_Demoxxx_xxxBed = open(( p + '\\DESsimulation\\data\\%s.csv' %(name)), mode='w', newline='')
    writer = csv.writer(data_Demoxxx_xxxBed)
    writer.writerow(['h_id','AvgDailyPatients','ResourceNumber','AdditionalResourceNumber','TriageAdditionalResourceThresholds','TriageAdditionalResourceControlTime','TreatmentAdditionalResourceThresholds','TreatmentAdditionalResourceControlTime'])
    ResourceNumber = str(Demo_BED[2]).split()
    ResourceNumber[5] = bed
    ResourceNumber = " ".join(ResourceNumber)
    writer.writerow([Demo_BED[0],Demo_BED[1],ResourceNumber,Demo_BED[3],Demo_BED[4],Demo_BED[5],Demo_BED[6],Demo_BED[7]])
    data_Demoxxx_xxxBed.close()

    #create bed_releasetime.csv
    h_id = Demoxxx
    release_time_hr, release_time_min = 0, 0
    bed_releasetime = open(( p + '\\DESsimulation\\data\\bed_releasetime.csv'), mode='w', newline='')
    writer = csv.writer(bed_releasetime)
    writer.writerow(['run_id','h_id','bed_id','release_time_hr','release_time_min'])
    for run_id in range(1,301):
        for bed_id in range(1,int(bed)+1):
            writer.writerow([run_id,h_id,bed_id,release_time_hr,release_time_min])
    bed_releasetime.close()

    # capicity error
    if int(input("capicity == 0 : ")) == 1:
        data_Demoxxx_xxxBed = pd.read_csv( p + '\\DESsimulation\\data\\%s.csv' %(name))
        df = pd.DataFrame(data_Demoxxx_xxxBed)
        ARN = str(df["AdditionalResourceNumber"]).split()
        ARN[2] = '0'
        ARN = ' '.join(ARN[0:7])
        df.at[0,'AdditionalResourceNumber'] = ARN
        print(df["AdditionalResourceNumber"])
        export = df
        export.to_csv( p + '\\DESsimulation\\data\\%s.csv' %(name), index=False, encoding='big5')

    # file too big error
    if int(input("too big = ")) == 1:
        con = sqlite3.connect( p + "\\DESsimulation\\output\\" + name + "\\Queue_079g_TriTLO_1.sqlite")
        cur = con.cursor()
        cur.execute("Create Table Process_Time_079_avgday as \
                     SELECT nDay, AVG(Wait_for_Admission) as Q_for_Bed \
                     FROM Time_Records_079g_300 \
                     Group by Hospital, nDay, Type")
        sql_query = pd.read_sql_query('select * from Process_Time_079_avgday', con)
        df = pd.DataFrame(sql_query)
        df.to_csv( p + "\\DESsimulation\\output\\" + name + "\\Process_Time_079_avgday.csv", index=False)

    if int(input("done = ")) == 1:
        #create figure
        avgday = pd.read_csv( p + '\\DESsimulation\\output\\%s\\Process_Time_079_avgday.csv' %(name))
        x = avgday['nDay'].tolist()
        y = avgday['Q_for_Bed'].tolist()
        plt.figure(figsize=(10,6))
        plt.scatter(x,y)
        plt.axhline(y = 480, c='r')
        plt.title(name)
        plt.savefig( p + '\\DESsimulation\\output\\figure\\' + name)
        plt.show()
        plt.close()

        if int(input("upload = ")) == 1:
            #rename upload file
            oldname = p + '\\DESsimulation\\output\\' + name + '\\Queue_079g_TriTLO_1.sqlite'
            newname = p + '\\DESsimulation\\output\\' + name + "\\Demo%s_%s_Queue_079g_TriTLO_1.sqlite" %(demo,bed) 
            os.rename(oldname, newname)
            print("upload")

            #change hospital_ResourceNumber.csv
            hospital_ResourceNumber = pd.read_csv( p + '\\DESsimulation\\hospital_ResourceNumber.csv',encoding='big5')
            df2 = pd.DataFrame(hospital_ResourceNumber)
            print(df2['急診模擬病床資源數'])
            df2.loc[i,'急診模擬病床資源數'] = bed
            print(df2.loc[i,'急診模擬病床資源數'])
            print(df2.loc[i-1,'欄1'])
            df2.to_csv( p + '\\DESsimulation\\hospital_ResourceNumber.csv', index=False, encoding='big5')
        else:
            try: shutil.rmtree( p + '\\DESsimulation\\output\\' + name)
            except OSError as e: print(e)
            else: print("The directory is deleted successfully")