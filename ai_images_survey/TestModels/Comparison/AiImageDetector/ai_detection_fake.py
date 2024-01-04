import pandas as pd
from create_plot import *

df = pd.read_csv('../../AiImageDetector/csv/ResultsAiDetectorFake.csv')
plot_0_25(df)
plot_25_50(df)
plot_50_75(df)
plot_75_100(df)









