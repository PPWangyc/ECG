import numpy as np
import pandas as pd
import neurokit2 as nk

def calculate_rmssd(df,sample_rate):
    _, rpeaks = nk.ecg_peaks(df['ecg_data'], sampling_rate=sample_rate)

    nn_intervals = np.diff(rpeaks['ECG_R_Peaks'])

    rmssd = np.sqrt(np.mean(np.square(np.diff(nn_intervals))))

    return rmssd

def read_ecg_data(filename):
    # the file format is: 
    # Sample Rate: 500
    # Time (s),ECG (mV), Z0 (mV), dZ/dt (mV/s)
    # 0.000000,0.000000 ,0.000000 ,0.000000
    # read the data from the file and return each column as a list and sample rate
    with open(filename, 'r') as f:
        # read the first line
        first_line = f.readline()
        # get the sample rate
        sample_rate = float(first_line.split(':')[1].strip())
        # read the second line
        second_line = f.readline()
        # get the column name
        column_name = second_line.split(',')
        # read the data
        data = np.loadtxt(f, delimiter='\t')
        # get the data for each column
        time = data[:, 0]
        ecg_data = data[:, 1]
        z0_data = data[:, 2]
        dzdt_data = data[:, 3]
        # make time ecg_data z0_data dzdt_data to a pandas dataframe
        df = pd.DataFrame({'time': time, 'ecg_data': ecg_data, 'z0_data': z0_data, 'dzdt_data': dzdt_data})
        return sample_rate, df
