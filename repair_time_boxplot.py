from pickle import TRUE
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

path = 'D:\\NCREE\\DESsimulation'

data = pd.read_csv(path + '\\data\\repair_time.csv')
print(data.info())

# -1
for i in range(len(data.index)):
    if data['repair_time'][i] == -1:
        data = data.drop(i)
print(data.info())

# box plot
plt.figure()
box_plot = sns.boxplot(x='h_id', y='repair_time', hue='room_id', data=data, showmeans=TRUE, \
                       palette='Pastel1', saturation=0.5, fliersize=3, \
                       order=['Demo003', 'Demo005','Demo006', 'Demo007','Demo009', 'Demo010','Demo016', 'Demo017',])
box_plot.set_xlabel('Hospital', fontsize=14)
box_plot.set_ylabel('Downtime', fontsize=14)
plt.grid(True,color = 'gray' ,linewidth = '0.5',axis='both', alpha=0.25)
plt.legend(fontsize=12)   
plt.show()