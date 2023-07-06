import pandas as pd
import numpy as np

# read the data from csv file to a dataframe
df = pd.read_csv('Results-070523-withOverThreshold.csv')
# delete rows which does not contains '_'
df = df[df['ExternalIdentifier'].str.contains('_')]
# delete the rows contain string'testing'
df = df[~df['ExternalIdentifier'].str.contains('testing')]
df = df[~df['ExternalIdentifier'].str.contains('1b')]
df = df[~df['ExternalIdentifier'].str.contains('6v2')]
# get subject id and session id from df['ExternalIdentifier'], and make them as two new columns
df['subject_id'] = df['ExternalIdentifier'].str.split('_').str[1]
df['session_id'] = df['ExternalIdentifier'].str.split('_').str[0]
# delete external identifier column
df = df.drop(columns=['ExternalIdentifier'])

# convert subject id and seesion id to int, some of them are subject99, convert them to 99, some is 010, convert them to 10
df['subject_id'] = df['subject_id'].str.replace('session', '').astype(int)
df['session_id'] = df['session_id'].str.replace('subject', '').astype(int)
# select subject 1, session 1-3, 7-9, 13-15;subject 2 session 4-6, 10 -12, 16-18
# df_1 = df[(df['subject_id'] == 1) & (df['session_id'].isin([1, 2, 3, 7, 8, 9, 13, 14, 15]))]
# df_2 = df[(df['subject_id'] == 2) & (df['session_id'].isin([4, 5, 6, 10, 11, 12, 16, 17, 18]))]
# df_3 = df[(df['subject_id'] == 3) & (df['session_id'].isin([1, 2, 3, 7, 8, 9, 13, 14, 15]))]
# df_4 = df[(df['subject_id'] == 4) & (df['session_id'].isin([4, 5, 6, 10, 11, 12, 16, 17, 18]))]
# df_5 = df[(df['subject_id'] == 5) & (df['session_id'].isin([1, 2, 3, 7, 8, 9, 13, 14, 15]))]
# df_6 = df[(df['subject_id'] == 6) & (df['session_id'].isin([4, 5, 6, 10, 11, 12, 16, 17, 18]))]
# df_7 = df[(df['subject_id'] == 7) & (df['session_id'].isin([1, 2, 3, 7, 8, 9, 13, 14, 15]))]
# df_8 = df[(df['subject_id'] == 8) & (df['session_id'].isin([4, 5, 6, 10, 11, 12, 16, 17, 18]))]

# concatenate the dataframes
# df= pd.concat([df_1, df_2, df_3, df_4, df_5, df_6, df_7, df_8])

# read json file
import json
# the df['Results] is a json string, convert it to a json object
df['Results'] = df['Results'].apply(json.loads)
# the dict is 'results':[{'time':292,'res':'S'}, ..]
# compute average of time in results where the 'res' is 'S'
# df['Results'] = df['Results'].apply(lambda x: np.mean([item['time'] for item in x['results'] if item['res'] == 'S']))
# make subject id and session id to the first two columns
df = df[['subject_id', 'session_id', 'Results', 'Accuracy','Game_FK','StartLevel','OverThreshold','CreatedAt','CompletedAt']]
# rename the column results to time(average)
# df = df.rename(columns={'Results': 'reaction time(average)'})
# read xslx file to a dataframe, which xslx contains several sheets, I want to read the first sheet
df_2 = pd.read_excel('map.xlsx', sheet_name='Mixed Signals Difficulty')
df_3 = pd.read_excel('map.xlsx', sheet_name='Mixed Signals Threshold')
# only remain firs 8 rows
df_2 = df_2.iloc[:8]
df_3 = df_3.iloc[:8]
# remove the first column which is an Unamed
df_2 = df_2.drop(columns=['Unnamed: 0'])
df_3 = df_3.drop(columns=['Unnamed: 0'])
# make the row index start from 1
df_2.index = np.arange(1, len(df_2) + 1)
df_3.index = np.arange(1, len(df_3) + 1)
# convert df_2 columns name from Session_{num} to int num
df_2.columns = df_2.columns.str.replace('Session ', '')
df_3.columns = df_3.columns.str.replace('Session ', '')
# find the index and column name of non NaN value in df_2
index_list = df_2.stack().index[df_2.stack().notnull()]

# convert the index and column name to a list of tuple
index_list = list(index_list)
# make all tuple in index_list to int
index_list = [(int(item[0]), int(item[1])) for item in index_list]
# select rows in df where subject id and session id are in index_list
df = df[df.apply(lambda x: (x['subject_id'], x['session_id']) in index_list, axis=1)]
# add a new column called MOT Difficulty in df and match the value from df_2 according to subject id and session id, subject id is the row index, session id is the column name
df['Difficulty'] = df.apply(lambda x: df_2.loc[x['subject_id'], str(x['session_id'])], axis=1)
# add a new column called MOT Threshold in df and match the value from df_3 according to subject id and session id, subject id is the row index, session id is the column name
df['Threshold'] = df.apply(lambda x: df_3.loc[x['subject_id'], str(x['session_id'])], axis=1)
# add another column called block id, which start from 1 and increase by 1 when subject id, session id changes
df['block_id'] = df.groupby(['subject_id', 'session_id']).cumcount() + 1
print(df)
# save the dataframe to csv file
df.to_csv('temp.csv', index=False)