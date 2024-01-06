import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('csv/PredictionsFakeNewsImagesCNN.csv')

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
new_df.drop_duplicates(subset='File_name', inplace=True)

grouped_df = new_df.groupby('Date').size().reset_index(name='Count')
grouped_df['Percentage'] = (grouped_df['Count'] / new_df.shape[0])

grouped_df = grouped_df.sort_values(by='Percentage', ascending=True)

plt.figure(figsize=(12, 9))
plt.barh(grouped_df['Date'], grouped_df['Count'])
plt.title(f'Numero di immagini fake per anno (Dataset Fake News)', fontsize=16)
plt.xlabel(f'Quantità su un totale di {new_df.shape[0]}', fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.show()

new_df.to_csv('csv/PredictionFakeNewsImagesCNN50.csv', index=False)


