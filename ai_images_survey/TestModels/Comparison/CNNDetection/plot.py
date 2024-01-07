from ai_images_survey.TestModels.Comparison.create_plot_fake import *
from ai_images_survey.TestModels.Comparison.create_plot_real import *

df_fake = pd.read_csv('../../CNNDetection/csv/ResultsCNNFake.csv')
df_real = pd.read_csv('../../CNNDetection/csv/ResultsCNNReal.csv')

plot_50_100(df_fake, 'CNNDetection')
plot_real(df_real, 'CNNDetection')








