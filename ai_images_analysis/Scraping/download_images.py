import os
import re
import pandas as pd
import requests

def download_images(img_url, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

    img_data = requests.get(img_url).content

    basename = os.path.basename(img_url)
    basename = os.path.splitext(basename)[0]
    basename = re.sub(r'[^a-zA-Z0-9_.-]', '_', basename)

    img_path = os.path.join(folder, basename+'.png')

    with open(img_path, 'wb') as img_file:
        img_file.write(img_data)


df = pd.read_csv('name_dataset.csv')

for i in range(0, df.shape[0]):
    print(i)
    urls = str(df.loc[i]['Images_url'])
    urls = urls.split(sep='SEPARATORLINK')
    for url in urls:
        try:
            download_images(url, str(df.loc[i]['Index']))
        except Exception as e:
            print(e)
