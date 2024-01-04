import os
import pandas as pd
import requests
from config import API_TOKEN

results = {
    'Path': [],
    'Model': [],
    'Verdict': []
}

counter = 0

url = "https://api.aiornot.com/v1/reports/image"

payload = {}

headers = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Accept': 'application/json'
}


def make_prediction(file_path):
    files = [
        ('object', (file_path, open(file_path, 'rb'), f'image/{file_path.split(".")[-1]}')),
    ]
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    verdict = None
    if response.status_code == 200:
        verdict = response.json()['report']['verdict']
    return verdict


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
        results['Verdict'].append(result)
        counter += 1
        print(counter)


# subset of FakeImagesDataset with only 100 images where CNNDetector has had problems
dir_path = [
    'FakeImagesDatasetAIorNot/BigGAN',
    'FakeImagesDatasetAIorNot/CycleGAN',
    'FakeImagesDatasetAIorNot/Dall-e3',
    'FakeImagesDatasetAIorNot/GANFormer',
    'FakeImagesDatasetAIorNot/GauGAN',
    'FakeImagesDatasetAIorNot/Glide',
    'FakeImagesDatasetAIorNot/IF',
    'FakeImagesDatasetAIorNot/Midjourney5',
    'FakeImagesDatasetAIorNot/ProGAN',
    'FakeImagesDatasetAIorNot/SD1.5',
    'FakeImagesDatasetAIorNot/SD2.1',
    'FakeImagesDatasetAIorNot/StarGAN',
    'FakeImagesDatasetAIorNot/StyleGAN1',
    'FakeImagesDatasetAIorNot/StyleGAN2',
    'FakeImagesDatasetAIorNot/StyleGAN3',
]

for folder in dir_path:
    iter_folder(folder, make_prediction)

# iter_folder('RealImagesDatasetAIorNot', make_prediction)

df = pd.DataFrame.from_dict(results)
df.to_csv('csv/ResultsAIorNotFake.csv', index=False)
# df.to_csv('csv/ResultsAIorNotReal.csv', index=False)

