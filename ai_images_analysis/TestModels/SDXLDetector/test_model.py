import os
import pandas as pd
from transformers import pipeline
import torch

results = {
    'Path': [],
    'Model': [],
    '%Syntetic': []
}

counter = 0

device = torch.device("cuda")
pipe = pipeline("image-classification", model="Organika/sdxl-detector", device=device)


def make_prediction(file_path):
    result = pipe(file_path)
    print(result)
    if result[0]['label'] == 'artificial':
        formatted_result = '{:.2f}'.format(float(result[0]['score'])*100)
    else:
        formatted_result = '{:.2f}'.format(float(result[1]['score'])*100)
    print(formatted_result)
    return formatted_result


def iter_folder(folder, prediction_function):
    global counter

    if not os.path.isdir(folder):
        print(f"{folder} isn't valid folder.")
        return

    list_file = os.listdir(folder)

    for file in list_file:
        file_path = os.path.join(folder, file)
        result = prediction_function(file_path)
        results['Path'].append(file)
        results['Model'].append(folder.split("/")[-1])
        results['%Syntetic'].append(result)
        counter += 1
        print(counter)


dir_path = [
    '../FakeImagesDataset/BigGAN',
    '../FakeImagesDataset/CycleGAN',
    '../FakeImagesDataset/Dall-e3',
    '../FakeImagesDataset/GANFormer',
    '../FakeImagesDataset/GauGAN',
    '../FakeImagesDataset/Glide',
    '../FakeImagesDataset/IF',
    '../FakeImagesDataset/Midjourney5',
    '../FakeImagesDataset/ProGAN',
    '../FakeImagesDataset/SD1.5',
    '../FakeImagesDataset/SD2.1',
    '../FakeImagesDataset/StarGAN',
    '../FakeImagesDataset/StyleGAN1',
    '../FakeImagesDataset/StyleGAN2',
    '../FakeImagesDataset/StyleGAN3',
]


# for folder in dir_path:
#     iter_folder(folder, make_prediction)

iter_folder('../RealImagesDataset', make_prediction)

df = pd.DataFrame.from_dict(results)
# df.to_csv('csv/ResultsSDXLDetectorFake.csv', index=False)
df.to_csv('csv/ResultsSDXLDetectorReal.csv', index=False)