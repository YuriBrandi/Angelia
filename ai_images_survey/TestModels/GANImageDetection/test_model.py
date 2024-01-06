import os
import pandas as pd
from PIL import Image
from resnet50nodown import resnet50nodown
import torch
import torch.nn
import torchvision.transforms as transforms
from torch.cuda import is_available as is_available_cuda

results = {
    'Path': [],
    'Model': [],
    '%Syntetic': []
}

counter = 0

device = 'cuda:0' if is_available_cuda() else 'cpu'
model = resnet50nodown(device, 'weights/gandetection_resnet50nodown_stylegan2.pth')

# Transform images using torchvision
trans = transforms.Compose([
    transforms.ToTensor(),  # transform img in tensor
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),  # normalize img
])

def make_prediction(file_path):
    # open image and apply transformation
    img = trans(Image.open(file_path).convert('RGB'))

    # make prediction
    with torch.no_grad():  # disable compute gradient
        in_tens = img.unsqueeze(0)  # create input tensor with batch dimension equals 1
        in_tens = in_tens.cuda()  # move the tensor on GPU
        prob = model(in_tens).sigmoid().item()

    formatted_result = '{:.2f}'.format(prob * 100)
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
#
iter_folder('../RealImagesDataset', make_prediction)
#
df = pd.DataFrame.from_dict(results)
# df.to_csv('csv/ResultsCNNFake.csv', index=False)
df.to_csv('csv/ResultsGANReal.csv', index=False)