import pandas as pd
from matplotlib import pyplot as plt


def plot_real(df: pd.DataFrame, model: str):
    df_filtered0 = df[df['%Syntetic'] <= 25]
    df_filtered1 = df[(df['%Syntetic'] > 25) & (df['%Syntetic'] <= 50)]
    df_filtered2 = df[(df['%Syntetic'] > 50) & (df['%Syntetic'] <= 75)]
    df_filtered3 = df[(df['%Syntetic'] > 75) & (df['%Syntetic'] <= 100)]

    new_df = pd.DataFrame({'Entry': ['Prob. 0-25', 'Prob. 25-50', 'Prob. 50-75', 'Prob. 75-100'],
                           'Percentage': [(df_filtered0.size / df.size),
                                          (df_filtered1.size / df.size),
                                          (df_filtered2.size / df.size),
                                          (df_filtered3.size / df.size)]})

    # sort the new dataframe
    new_df = new_df.sort_values(by='Percentage', ascending=True)

    plt.figure(figsize=(12, 9))
    plt.barh(new_df['Entry'], new_df['Percentage'])
    plt.title(f'Percentuale di immagini reali con probabilità di essere sintetiche ({model})', fontsize=16)
    plt.xlabel('Percentuale rispetto al totale delle immagini per ciascun gruppo (0-1)', fontsize=14)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    plt.show()