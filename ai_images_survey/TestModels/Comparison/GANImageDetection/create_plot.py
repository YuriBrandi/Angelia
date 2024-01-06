import matplotlib.pyplot as plt
import pandas as pd


def plot_50_100(df_original):
    new_models_row = pd.DataFrame({'Model': ['SD2.1', 'Midjourney5'], 'Count': [0,0]})
    df_filtered = pd.concat([df_original[(df_original['%Syntetic'] <= 100) & (df_original['%Syntetic'] > 50)],
                             new_models_row], ignore_index=True)
    grouped_df = _new_dataframe_for_plot(df_original, df_filtered)
    _plot(grouped_df, 50, 100)


def _new_dataframe_for_plot(df_original, df_filtered):
    # create new dataframe for plot
    grouped_df = df_filtered.groupby('Model').size().reset_index(name='Count')
    grouped_df['TotalImagesPerModel'] = df_original.groupby('Model').size().reset_index(name='TotalImages')[
        'TotalImages']
    grouped_df['Percentage'] = (grouped_df['Count'] / grouped_df['TotalImagesPerModel'])

    # sort the new dataframe
    grouped_df = grouped_df.sort_values(by='Percentage', ascending=True)
    return grouped_df


def _plot(grouped_df, range1, range2):
    plt.figure(figsize=(12, 9))
    plt.barh(grouped_df['Model'], grouped_df['Percentage'])
    if range1 == 0 and range2 == 25:
        plt.title(f'Percentuale di immagini sintetiche con probabilità {range1} <= p < {range2} (GAN Image Detection)',
                  fontsize=16)
    else:
        plt.title(f'Percentuale di immagini sintetiche con probabilità {range1} < p <= {range2} (GAN Image Detection)',
                  fontsize=16)
    plt.xlabel('Percentuale rispetto al totale delle immagini per ciascun gruppo (0-1)', fontsize=14)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.show()