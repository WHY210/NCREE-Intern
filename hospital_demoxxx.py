# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 10:18:38 2022

@author: hywu
"""
import pandas as pd
import csv

hospital = [3,5,6,7,9,10,16,17]
for j in range(len(hospital)):
    i = hospital[j] - 1
    
    # read hospital_ResourceNumber
    hospital_ResourceNumber = pd.read_csv("C:\\Users\\hywu\\Desktop\\DES\\hospital_ResourceNumber.csv", encoding='big5')
    Demoxxx = str(hospital_ResourceNumber['h_id'].tolist()[i])
    Days = int(hospital_ResourceNumber['平均住院日'].tolist()[i])    

    # create new Demoxxx.csv
    Admission = str((Days-2)*24*60) + " " + str((Days+2)*24*60) + " " + str(Days*24*60)  
    hospital_Demoxxx = open('C:\\Users\\hywu\\Desktop\\DES\\hospital\\%s.csv' %(Demoxxx), mode='w', newline='')
    writer = csv.writer(hospital_Demoxxx)
    writer.writerow([''           ,'Triage'  ,'Treatment'  ,'Xray'    ,'Observation','Operation'  ,'Admission','OccupyResource','Priority'])
    writer.writerow(['AL1+AL2(op)','2.25 0.7','7.5 45 22.5','1.25 9.2','0 7.5 30'   ,'120 480 240', Admission ,'1 2 1 1 1 1'   ,'1'])
    writer.writerow(['AL1+AL2'	  ,'4.5 0.7' ,'15 90 45',   '2.5 9.2' ,'0 15 60'    ,'120 480 240', Admission ,'1 1 1 1 1 1'   ,'2'])
    writer.writerow(['AL3'	      ,'4.5 0.7' ,'15 90 45',	'2.5 9.2' ,'0 15 60'    ,'120 480 240', Admission ,'1 1 1 1 1 1'   ,'3'])
    writer.writerow(['AL4'	      ,'4.5 0.7' ,'15 90 45',	'2.5 9.2' ,'0 15 60'    ,'120 480 240', Admission ,'1 1 1 1 1 1'   ,'3'])
    writer.writerow(['AL5'	      ,'4.5 0.7' ,'15 90 45',	'2.5 9.2' ,'0 15 60'    ,'120 480 240', Admission ,'1 1 1 1 1 1'   ,'3'])
    hospital_Demoxxx.close()    

