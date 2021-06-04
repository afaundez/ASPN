import os
import tensorflow as tf
import torch.utils.data as data
from torch import nn
from torch.nn import functional as F
from torchvision import models
import torchvision
from PIL import Image
import os.path

def conv3x3(in_, out):
    return nn.Conv2d(in_, out, 3, padding=1)

class ConvRelu(nn.Module):
    def __init__(self, in_, out):
        super().__init__()
        self.conv = conv3x3(in_, out)
        self.conv = conv1x1(in_, out)
        self.activation = nn.ReLU(inplace=True)

IMG_EXTENSIONS = [
    '.jpg', '.JPG', '.jpeg', '.JPEG',
    '.png', '.PNG', '.ppm', '.PPM', '.bmp', '.BMP',
]

NPY_EXTENSIONS = [
    '.npy'
]

def is_image_file(filename):
    return any(filename.endswith(extension) for extension in IMG_EXTENSIONS)


def is_numpy_file(filename):
    return any(filename.endswith(extension) for extension in NPY_EXTENSIONS)

def make_dataset(dir):
    images = []
    assert os.path.isdir(dir), '%s is not a valid directory' % dir

    for root, _, fnames in sorted(os.walk(dir)):
        for fname in fnames:
            if is_image_file(fname):
                path = os.path.join(root, fname)
                images.append(path)

    return images

def make_geo_dataset(dir):
    images = []
    assert os.path.isdir(dir), '%s is not a valid directory' % dir
    dir_rgbir  = os.path.join(dir, 'RGBIRImages')
    dir_label = os.path.join(dir, 'LabelImages')

    for root, _, fnames in sorted(os.walk(dir_rgbir)):
        for fname in fnames:
            if is_numpy_file(fname):
                path_rgbir = os.path.join(root, fname)
                fn, file_extension = os.path.splitext(fname)
                path_label = os.path.join(dir_label, fn + '.npy')
                images.append({'A' : path_rgbir, 'B' : path_label})

    return images

def default_loader(path):
    return Image.open(path).convert('RGB')


class ImageFolder(data.Dataset):

    def __init__(self, root, transform=None, return_paths=False,
                 loader=default_loader):
        imgs = make_dataset(root)
        if len(imgs) == 0:
            raise(RuntimeError("Found 0 images in: " + root + "\n"
                               "Supported image extensions are: " +
                               ",".join(IMG_EXTENSIONS)))

 #       self.root = root
 #      self.imgs = imgs
        self.transform = transform
        self.return_paths = return_paths
        self.loader = loader

    def __getitem__(self, index):
        path = self.imgs[index]
        img = self.loader(path)
        if self.transform is not None:
            img = self.transform(img)
        if self.return_paths:
            return img, path
        else:
            return img

    def __len__(self):
        return len(self.imgs)
