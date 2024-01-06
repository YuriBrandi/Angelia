from create_plot import *

df = pd.read_csv('../../CNNDetection/csv/ResultsCNNFake.csv')
plot_0_25(df)
plot_25_50(df)
plot_50_75(df)
plot_75_100(df)
plot_50_100(df)
