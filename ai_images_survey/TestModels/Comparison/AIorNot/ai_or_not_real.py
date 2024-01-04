from itertools import cycle
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('../../AIorNot/csv/ResultsAIorNotReal.csv')

df_human = df[df['Verdict'] == 'human']
df_ai = df[df['Verdict'] == 'ai']

new_df = pd.DataFrame({'Entry': ['AI', 'Human'],
                       'Percentage': [(df_ai.size / df.size),
                                      (df_human.size / df.size),
                                      ]})

# sort the new dataframe
new_df = new_df.sort_values(by='Percentage', ascending=True)

plt.figure(figsize=(12, 9))

colors = cycle(plt.rcParams['axes.prop_cycle'].by_key()['color'])
blue = next(colors)
orange = next(colors)
plt.barh(new_df['Entry'], new_df['Percentage'], color=[orange, blue])
plt.title('Percentuale di verdetti per ogni immagine reale (AIorNot)', fontsize=16)
plt.xlabel('Percentuale (0-1)', fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

plt.show()