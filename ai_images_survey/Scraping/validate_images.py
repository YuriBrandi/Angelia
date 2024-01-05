from PIL import Image
import os
import pandas as pd


def is_image_openable(file_path):
    try:
        with Image.open(file_path):
            return True
    except (IOError, OSError, Image.DecompressionBombError):
        return False


def delete_unopenable_images(directory_path):
    if not os.path.exists(directory_path):
        return

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path) and is_image_openable(file_path):
            print(f"L'immagine in {file_path} è apribile.")
        else:
            try:
                os.remove(file_path)
                print(f"L'immagine non apribile in {file_path} è stata eliminata.")
            except Exception as e:
                print(e)


def delete_empty_folder(directory_path):
    if not os.path.exists(directory_path):
        return
    if not os.listdir(directory_path):
        os.rmdir(directory_path)


df = pd.read_csv('csv/DatasetFakeNewsImagesWithUrl.csv')

for i in range(0, df.shape[0]):
    directory_path = f"FakeNewsImagesDataset/{i}"
    # delete_empty_folder(directory_path)
    delete_unopenable_images(directory_path)
