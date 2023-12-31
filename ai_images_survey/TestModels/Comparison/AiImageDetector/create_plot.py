import matplotlib.pyplot as plt


def plot_0_25(df_original):
    df_filtered = df_original[df_original['%Syntetic'] <= 25]
    grouped_df = _new_dataframe_for_plot(df_original, df_filtered)
    _plot(grouped_df, 0, 25)


def plot_25_50(df_original):
    df_filtered = df_original[(df_original['%Syntetic'] > 25) & (df_original['%Syntetic'] <= 50)]
    grouped_df = _new_dataframe_for_plot(df_original, df_filtered)
    _plot(grouped_df, 25, 50)


def plot_50_75(df_original):
    df_filtered = df_original[(df_original['%Syntetic'] > 50) & (df_original['%Syntetic'] <= 75)]
    grouped_df = _new_dataframe_for_plot(df_original, df_filtered)
    _plot(grouped_df, 50, 75)


def plot_75_100(df_original):
    df_filtered = df_original[(df_original['%Syntetic'] > 75) & (df_original['%Syntetic'] <= 100)]
    grouped_df = _new_dataframe_for_plot(df_original, df_filtered)
    _plot(grouped_df, 75, 100)


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
    plt.title(f'Percentuale di immagini sintetiche con probabilità {range1} <= p < {range2} (Ai-image-detector)',
              fontsize=16)
    plt.xlabel('Percentuale rispetto al totale delle immagini per ciascun gruppo (0-1)', fontsize=14)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.show()