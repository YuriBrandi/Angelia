import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('csv/PredictionFakeNewsImages.csv')

new_df = {'Index': [], 'File_name': [], 'Link_news': [], 'Topic': [], 'Date': [], '%Syntetic': []}

print(df.shape)

for i in range(0, df.shape[0]):
    if float(df.loc[i]['%Syntetic']) > 50.00:
        for col in df.columns:
            if col == 'Date':
                new_df[col].append(str(df.loc[i][col]).split('-')[0])
            else:
                new_df[col].append(df.loc[i][col])

new_df = pd.DataFrame.from_dict(new_df)
new_df2 = new_df.copy()
new_df.drop_duplicates(subset='File_name', inplace=True)

grouped_df = new_df.groupby('Date').size().reset_index(name='Count')
grouped_df = grouped_df.sort_values(by='Count', ascending=True)

#new_df2.drop_duplicates(subset='Index', inplace=True)
#grouped_df2 = new_df2.groupby(['Date']).size().reset_index(name='Count')

plt.figure(figsize=(12, 9))
plt.barh(grouped_df['Date'], grouped_df['Count'])
plt.title(f'Numero di immagini fake per anno (Dataset Fake News)', fontsize=16)
plt.xlabel(f'Quantità su un totale di {new_df.shape[0]}', fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.show()

new_df.to_csv('csv/PredictionFakeNewsImagesDrop.csv', index=False)
print(grouped_df)

diz = {'2016':0, '2017':0, '2018':0, '2020':0, '2021':0, '2022':0, '2023':0}
count = {'2016':0, '2017':0, '2018':0, '2020':0, '2021':0, '2022':0, '2023':0}
avg = {'2016':0, '2017':0, '2018':0, '2020':0, '2021':0, '2022':0, '2023':0}

new_df2.reset_index(inplace=True)
for i in range(0, new_df2.shape[0]):
    for y in range(2016, 2024):
        if int(new_df2.loc[i]['Date']) == y:
            diz[f'{y}'] += float(new_df2.loc[i]['%Syntetic'])
            count[f'{y}'] += 1

for y in avg.keys():
    avg[f'{y}'] = diz[f'{y}'] / count[f'{y}']

print(avg)
