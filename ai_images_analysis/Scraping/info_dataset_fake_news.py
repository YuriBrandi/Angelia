import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('csv/FakeNewsImagesWithUrlDataset.csv')

for i in range(0, df.shape[0]):
    year = str(df.loc[i]['Date']).split('-')[0]
    df.loc[i, 'Date'] = year

grouped_df = df.groupby('Date').size().reset_index(name='Count')
grouped_df2 = df.groupby('Topic').size().reset_index(name='Count')
grouped_df3 = df.groupby(['Topic', 'Date']).size().reset_index(name='Number of News')

print('DATASET GROUPED FOR DATE')
print(grouped_df)

print('\nDATASET GROUPED FOR TOPIC')
print(grouped_df2)

print('\nDATASET GROUPED FOR TOPIC AND DATE')
print(grouped_df3)