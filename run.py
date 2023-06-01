from utils import *
import os
# get all the folder path under the data_dir
data_dir = '/Users/yanchenwang/Data/T1'
folder_list = os.listdir(data_dir)

processed_ecg_df = pd.DataFrame(columns=['ecg_file', 'rmssd'])
# read all the data under the folder
for folder in folder_list:
    # get the path of the folder
    folder_path = os.path.join(data_dir, folder)
    # get all the file name under the folder
    file_list = os.listdir(folder_path)
    # read all the data under the folder
    for file in file_list:
        # get the path of the file
        file_path = os.path.join(folder_path, file)
        print("file_path:", file_path)
        # if the file is not a txt file, skip it
        if not file.endswith('.txt'):
            continue
        if 'ACT' in file:
            continue
        # read the data
        sample, df = read_ecg_data(file_path)
        # calculate the RMSSD
        rmssd = calculate_rmssd(df, sample)
        # print the result
        # add the result to the dataframe
        processed_ecg_df = processed_ecg_df._append({'ecg_file': file, 'rmssd': rmssd}, ignore_index=True)
        print("RMSSD:", rmssd)
        # exit()
print(processed_ecg_df)
# calculate the mean and std of task rmssd
task_rmssd = processed_ecg_df[processed_ecg_df['ecg_file'].str.contains('task')]['rmssd']
print("task_rmssd:", task_rmssd)
print("task_rmssd_mean:", task_rmssd.mean())
print("task_rmssd_std:", task_rmssd.std())
# calculate the mean and std of rest rmssd
rest_rmssd = processed_ecg_df[processed_ecg_df['ecg_file'].str.contains('rest')]['rmssd']
print("rest_rmssd:", rest_rmssd)
print("rest_rmssd_mean:", rest_rmssd.mean())
print("rest_rmssd_std:", rest_rmssd.std())

# conduct t-test
from scipy import stats
t, p = stats.ttest_ind(task_rmssd, rest_rmssd)
print("t:", t)
print("p:", p)

# plot the distribution of task and rest rmssd
import seaborn as sns
import matplotlib.pyplot as plt
# make x label from min to max with step 30
x = np.arange(min(processed_ecg_df['rmssd']), max(processed_ecg_df['rmssd']), 10)
# plot the distribution of task rmssd
sns.distplot(task_rmssd, bins=x, label='Task', color='red')
# plot the distribution of rest rmssd
sns.distplot(rest_rmssd, bins=x, label='Rest', color='blue')
plt.xlabel('RMSSD')
plt.ylabel('Density')
plt.legend()
plt.savefig('rmssd.png')
plt.close()

# plot the distribution of task
x = np.arange(min(task_rmssd), max(task_rmssd), 10)
sns.distplot(task_rmssd, bins=x, label='Task', color='red')
plt.xlabel('RMSSD(ms)')
plt.ylabel('Density')
plt.legend()
plt.savefig('task_rmssd.png')
plt.close()

# plot the distribution of rest
x = np.arange(min(rest_rmssd), max(rest_rmssd), 10)
sns.distplot(rest_rmssd, bins=x, label='Rest', color='blue')
plt.xlabel('RMSSD(ms)')
plt.ylabel('Density')
plt.legend()
plt.savefig('rest_rmssd.png')
plt.close()

# save the processed data
processed_ecg_df.to_csv('processed_ecg_df.csv', index=False)



