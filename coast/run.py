import pandas
import heartpy as hp
import matplotlib.pyplot as plt

# read txt file to pandas dataframe
ecg_data = pandas.read_csv('ECG2Data_epigg_0119202420_26_05_459.txt', header=None)
print(ecg_data.head())

# get the first column as values
ecg_data = ecg_data.iloc[:, 0].values
ecg_len = len(ecg_data)

working_data, measures = hp.process(ecg_data[int(0*ecg_len):int(1 * ecg_len)],1000)

plot_object = hp.plotter(working_data, measures, title = 'Heart rate signal peak detection, rmssd: %.3f'%measures['rmssd'])

# rmssd
print("rmssd: ", measures['rmssd'])

# show plot
plt.show()