import torch
from PIL import Image
from transformers import pipeline
from ai_images_survey.TestModels.GANImageDetection.resnet50nodown import resnet50nodown
import os
import torchvision.transforms as transforms
from torch.cuda import is_available as is_available_cuda
import pandas as pd

results = {
    'Index': [],
    'File_name': [],
    'Link_news': [],
    'Topic': [],
    'Date': [],
    '%Syntetic': []
}

# GAN Image Detection Model for fake news where 2015 <= year <= 2019
device = 'cuda:0' if is_available_cuda() else 'cpu'
model = resnet50nodown(device, '../TestModels/GANImageDetection/weights/gandetection_resnet50nodown_stylegan2.pth')

# Transform images using torchvision
trans = transforms.Compose([
    transforms.ToTensor(),  # transform img in tensor
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),  # normalize img
])


# SDXL Detector Model for fake news where 2019 < year <= 2023
pipe = pipeline("image-classification", model="Organika/sdxl-detector", device=device)


def make_prediction_sdxl(file_path):
    result = pipe(file_path)
    print(result)
    if result[0]['label'] == 'artificial':
        formatted_result = '{:.2f}'.format(float(result[0]['score'])*100)
    else:
        formatted_result = '{:.2f}'.format(float(result[1]['score'])*100)
    print(formatted_result)
    return formatted_result


def make_prediction_gan(file_path):
    # open image and apply transformation
    img = trans(Image.open(file_path).convert('RGB'))

    # make prediction
    with torch.no_grad():                       # disable compute gradient
        in_tens = img.unsqueeze(0)              # create input tensor with batch dimension equals 1
        in_tens = in_tens.cuda()                # move the tensor on GPU
        prob = model(in_tens).sigmoid().item()

    formatted_result = '{:.2f}'.format(prob * 100)
    return formatted_result


def iter_folder(index, link, topic, date, folder, prediction_function):

    if not os.path.isdir(folder):
        print(f"{folder} isn't valid folder.")
        return

    list_file = os.listdir(folder)

    for file in list_file:
        file_path = os.path.join(folder, file)
        try:
            result = prediction_function(file_path)
        except Exception as e:
            results['Index'].append(index)
            results['File_name'].append(file)
            results['Link_news'].append(link)
            results['Topic'].append(topic)
            results['Date'].append(date)
            results['%Syntetic'].append(None)
            continue
        results['Index'].append(index)
        results['File_name'].append(file)
        results['Link_news'].append(link)
        results['Topic'].append(topic)
        results['Date'].append(date)
        results['%Syntetic'].append(result)
    print(index)


df = pd.read_csv('../Scraping/csv/DatasetFakeNewsImagesWithUrl.csv')

for i in range(0, df.shape[0]):
    index = df.loc[i]['Index']
    topic = df.loc[i]['Topic']
    date = df.loc[i]['Date']
    link = df.loc[i]['Link']
    year = str(date).split('-')[0]
    if int(year) <= 2019:
        iter_folder(index, link, topic, date, f'Scraping/FakeNewsImagesDataset/{i}', make_prediction_gan)
    if int(year) > 2019:
        iter_folder(index, link, topic, date, f'Scraping/FakeNewsImagesDataset/{i}', make_prediction_sdxl)

df_new = pd.DataFrame.from_dict(results)
df_new.to_csv('csv/PredictionsFakeNewsImages.csv', index=False)

