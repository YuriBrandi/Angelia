from ai_images_survey.TestModels.CNNDetection.resnet import resnet50
import os
import torch
import torch.nn
import torchvision.transforms as transforms
from PIL import Image
import pandas as pd

results = {
    'Index': [],
    'File_name': [],
    'Link_news': [],
    'Topic': [],
    'Date': [],
    '%Syntetic': []
}

problems = []

# instance of Resnet-50 with 1 output class
model = resnet50(num_classes=1)
# load pre-trained weights on cpu
state_dict = torch.load('../TestModels/CNNDetection/weights/blur_jpg_prob0.5.pth', map_location='cpu')
# load weights on model
model.load_state_dict(state_dict['model'])

# move the model on GPU
model.cuda()
# set the model in evaluation mode
model.eval()

# Transform images using torchvision
trans = transforms.Compose([
    transforms.ToTensor(),  # transform img in tensor
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),  # normalize img
])


def make_prediction(file_path):
    # open image and apply transformation
    img = trans(Image.open(file_path).convert('RGB'))

    # make prediction
    with torch.no_grad():               # disable compute gradient
        in_tens = img.unsqueeze(0)      # create input tensor with batch dimension equals 1
        in_tens = in_tens.cuda()        # move the tensor on GPU
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
            problems.append(file_path)
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
    iter_folder(index, link, topic, date, f'Scraping/FakeNewsImagesDataset/{i}', make_prediction)

df_new = pd.DataFrame.from_dict(results)
df_new.to_csv('csv/PredictionsFakeNewsImagesCNN.csv', index=False)