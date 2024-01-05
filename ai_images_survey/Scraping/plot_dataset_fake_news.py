import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('csv/DatasetFakeNewsImagesWithUrl.csv')

for i in range(0, df.shape[0]):
    year = str(df.loc[i]['Date']).split('-')[0]
    df.loc[i, 'Date'] = year

grouped_df = df.groupby('Date').size().reset_index(name='Count')
grouped_df['Percentage'] = (grouped_df['Count'] / df.shape[0])

grouped_df = grouped_df.sort_values(by='Percentage', ascending=True)

plt.figure(figsize=(12, 9))
plt.barh(grouped_df['Date'], grouped_df['Percentage'])
plt.title(f'Percentuale di notizie per anno (Dataset Fake News)',
          fontsize=16)
plt.xlabel('Percentuale (0-1)', fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.show()

print(grouped_df)