import matplotlib.pyplot as plt
import pandas as pd


def plot_0_25(df_original):
    df_filtered = df_original[df_original['%Syntetic'] <= 25]
    grouped_df = _new_dataframe_for_plot(df_original, df_filtered)
    _plot(grouped_df, 0, 25)


def plot_25_50(df_original):
    new_models_row = pd.DataFrame({'Model': ['ProGAN'], 'Count': [0]})
    df_filtered = pd.concat([df_original[(df_original['%Syntetic'] > 25) & (df_original['%Syntetic'] <= 50)],
                             new_models_row], ignore_index=True)
    grouped_df = _new_dataframe_for_plot(df_original, df_filtered)
    _plot(grouped_df, 25, 50)


def plot_50_75(df_original):
    new_models_row = pd.DataFrame({'Model': ['ProGAN', 'SD2.1', 'Dall-e3'], 'Count': [0, 0, 0]})
    df_filtered = pd.concat([df_original[(df_original['%Syntetic'] > 50) & (df_original['%Syntetic'] <= 75)],
                             new_models_row], ignore_index=True)
    grouped_df = _new_dataframe_for_plot(df_original, df_filtered)
    _plot(grouped_df, 50, 75)


def plot_75_100(df_original):
    new_models_row = pd.DataFrame({'Model': ['SD2.1', 'Midjourney5'], 'Count': [0, 0]})
    df_filtered = pd.concat([df_original[(df_original['%Syntetic'] > 75) & (df_original['%Syntetic'] <= 100)],
                             new_models_row], ignore_index=True)
    grouped_df = _new_dataframe_for_plot(df_original, df_filtered)
    _plot(grouped_df, 75, 100)


def plot_50_100(df_original):
    new_models_row = pd.DataFrame({'Model': ['SD2.1'], 'Count': [0]})
    df_filtered = pd.concat([df_original[(df_original['%Syntetic'] <= 100) & (df_original['%Syntetic'] > 50)],
                            new_models_row], ignore_index=True)
    grouped_df = _new_dataframe_for_plot(df_original, df_filtered)
    _plot(grouped_df, 50, 100)


def _new_dataframe_for_plot(df_original, df_filtered, ranges=None):
    # create new dataframe for plot
    grouped_df = df_filtered.groupby('Model').size().reset_index(name='Count')
    grouped_df['TotalImagesPerModel'] = df_original.groupby('Model').size().reset_index(name='TotalImages')[
        'TotalImages']
    grouped_df['Percentage'] = (grouped_df['Count'] / grouped_df['TotalImagesPerModel'])

    if ranges == '25-50':
        # set 0 to ProGAN
        grouped_df.loc[grouped_df['Model'] == 'ProGAN', 'Percentage'] = 0
    elif ranges == '50-75':
        # set 0 to ProGAN, SD2-1, Dall-e3
        grouped_df.loc[grouped_df['Model'] == 'ProGAN', 'Percentage'] = 0
        grouped_df.loc[grouped_df['Model'] == 'SD2.1', 'Percentage'] = 0
        grouped_df.loc[grouped_df['Model'] == 'Dall-e3', 'Percentage'] = 0
    elif ranges == '75-100':
        # set 0 to SD2-1, Midjourney5
        grouped_df.loc[grouped_df['Model'] == 'Midjourney5', 'Percentage'] = 0
        grouped_df.loc[grouped_df['Model'] == 'SD2.1', 'Percentage'] = 0

    # sort the new dataframe
    grouped_df = grouped_df.sort_values(by='Percentage', ascending=True)
    return grouped_df


def _plot(grouped_df, range1, range2):
    plt.figure(figsize=(12, 9))
    plt.barh(grouped_df['Model'], grouped_df['Percentage'])
    if range1 == 0 and range2 == 25:
        plt.title(f'Percentuale di immagini sintetiche con probabilità {range1} <= p < {range2} (CNNDetection)',
                  fontsize=16)
    else:
        plt.title(f'Percentuale di immagini sintetiche con probabilità {range1} < p <= {range2} (CNNDetection)',
                  fontsize=16)
    plt.xlabel('Percentuale rispetto al totale delle immagini per ciascun modello (0-1)', fontsize=14)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.show()
