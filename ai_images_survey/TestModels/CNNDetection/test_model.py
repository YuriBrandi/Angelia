import os
import torch
import torch.nn
import torchvision.transforms as transforms
from PIL import Image
import pandas as pd
from resnet import resnet50

results = {
    'Path': [],
    'Model': [],
    '%Syntetic': []
}

counter = 0

# instance of Resnet-50 with 1 output class
model = resnet50(num_classes=1)
# load pre-trained weights on cpu
state_dict = torch.load('weights/blur_jpg_prob0.5.pth', map_location='cpu')
# load weights on model
model.load_state_dict(state_dict['model'])

# move the model on GPU
model.cuda()
# set the model in evaluation mode
model.eval()

# Transform images using torchvision
trans = transforms.Compose([
    transforms.ToTensor(),  # transform img in tensor
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),    # normalize img
])


def make_prediction(file_path):
    # open image and apply transformation
    img = trans(Image.open(file_path).convert('RGB'))

    # make prediction
    with torch.no_grad():                       # disable compute gradient
        in_tens = img.unsqueeze(0)              # create input tensor with batch dimension equals 1
        in_tens = in_tens.cuda()                # move the tensor on GPU
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
#     iter_folder(folder)

iter_folder('../RealImagesDataset', make_prediction)

df = pd.DataFrame.from_dict(results)
# df.to_csv('csv/ResultsCNNFake.csv', index=False)
df.to_csv('csv/ResultsCNNReal.csv', index=False)
