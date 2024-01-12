from ai_images_survey.TestModels.Comparison.create_plot_fake import *
from ai_images_survey.TestModels.Comparison.create_plot_real import *

df_fake = pd.read_csv('../../GANImageDetection/csv/ResultsGANFake.csv')
df_real = pd.read_csv('../../GANImageDetection/csv/ResultsGANReal.csv')

plot_50_100(df_fake, 'GAN Image Detection')
plot_real(df_real, 'GAN Image Detection')








