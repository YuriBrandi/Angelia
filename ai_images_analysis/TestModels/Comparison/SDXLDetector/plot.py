from ai_images_survey.TestModels.Comparison.create_plot_fake import *
from ai_images_survey.TestModels.Comparison.create_plot_real import *

df_fake = pd.read_csv('../../SDXLDetector/csv/ResultsSDXLDetectorFake.csv')
df_real = pd.read_csv('../../SDXLDetector/csv/ResultsSDXLDetectorReal.csv')

plot_50_100(df_fake, 'SDXL Detector')
plot_real(df_real, 'SDXL Detector')








