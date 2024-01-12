from ai_images_survey.TestModels.Comparison.create_plot_fake import *
from ai_images_survey.TestModels.Comparison.create_plot_real import *

df_fake = pd.read_csv('../../AiImageDetector/csv/ResultsAiDetectorFake.csv')
df_real = pd.read_csv('../../AiImageDetector/csv/ResultsAiDetectorFake.csv')

plot_50_100(df_fake, 'AI Image Detector')
plot_real(df_real, 'AI Image Detector')








