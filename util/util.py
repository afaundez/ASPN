from __future__ import print_function
import os
import tensorflow as tf
import torch
from PIL import Image
import numpy as np



# Converts a Tensor into an image array (numpy)
# |imtype|: the desired type of the converted numpy array
def tensor2im(input_image, imtype=np.uint8):
    if isinstance(input_image, torch.Tensor):
        image_tensor = input_image.data
    else:
        return input_image
    image_numpy = image_tensor[0].cpu().float().numpy()
    if image_numpy.shape[0] == 1:
        image_numpy = np.tile(image_numpy, (3, 1, 1))
    image_numpy = (np.transpose(image_numpy, (1, 2, 0)) + 1) / 2.0 * 255.0
    return image_numpy.astype(imtype)

# Converts a Tensor into an image array (numpy)
# |imtype|: the desired type of the converted numpy array
def tensor_label2im(input_image, imtype=np.uint8):
    if isinstance(input_image, torch.Tensor):
        image_tensor = input_image.data
    else:
        return input_image
    image_numpy = image_tensor[0].cpu().float().numpy()
    image_numpy = np.transpose(image_numpy, (1, 2, 0))

    colors = np.array(((1,1,1),(-1,-1,1),(-1,1,1),(-1,1,-1),(1,1,-1),(1,-1,-1)))
    out_size_f = image_numpy.shape[0]
    img = np.zeros((out_size_f, out_size_f, 3), dtype='float')
    img.fill(-1)
    for z in range(0,5):
        #TEMP
        #if z != 4:
        #    continue
        mask = image_numpy[:,:,z] >= -0.8
        color = colors[z]
        #color = np.flip(color, axis=0)
        img[mask,:] = color

    img = torch.from_numpy(img.transpose((2, 0, 1))).float()
    img = img[np.newaxis, ...]
    return img

def diagnose_network(net, name='network'):
    mean = 0.0
    count = 0
    for param in net.parameters():
        if param.grad is not None:
            mean += torch.mean(torch.abs(param.grad.data))
            count += 1
    if count > 0:
        mean = mean / count
    print(name)
    print(mean)


def save_image(image_numpy, image_path):
    image_pil = Image.fromarray(image_numpy)
    image_pil.save(image_path)


def print_numpy(x, val=True, shp=False):
    x = x.astype(np.float64)
    if shp:
        print('shape,', x.shape)
    if val:
        x = x.flatten()
        print('mean = %3.3f, min = %3.3f, max = %3.3f, median = %3.3f, std=%3.3f' % (
            np.mean(x), np.min(x), np.max(x), np.median(x), np.std(x)))


def mkdirs(paths):
    if isinstance(paths, list) and not isinstance(paths, str):
        for path in paths:
            mkdir(path)
    else:
        mkdir(paths)


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)
