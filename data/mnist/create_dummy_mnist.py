import numpy as np
import struct

import skimage.io as io

n_s = 200
to_print = 10


def loadlocal_mnist(images_path, labels_path):
    """Read MNIST from ubyte files.
    Parameters
    ----------
    images_path : str
        path to the test or train MNIST ubyte file
    labels_path : str
        path to the test or train MNIST class labels file
    Returns
    --------
    images : [n_samples, n_pixels] numpy.array
        Pixel values of the images.
    labels : [n_samples] numpy array
        Target class labels
    Examples
    -----------
    For usage examples, please see
    http://rasbt.github.io/mlxtend/user_guide/data/loadlocal_mnist/
    """
    with open(labels_path, "rb") as lbpath:
        magic, n = struct.unpack(">II", lbpath.read(8))
        labels = np.fromfile(lbpath, dtype=np.uint8)
    with open(images_path, "rb") as imgpath:
        magic, num, rows, cols = struct.unpack(">IIII", imgpath.read(16))
        images = np.fromfile(imgpath, dtype=np.uint8).reshape(len(labels), 784)

    return images, labels


data_x, data_y = loadlocal_mnist(
    "./train-images.idx3-ubyte", "./train-labels.idx1-ubyte"
)

index_3 = np.random.choice(np.where(data_y == 3)[0], size=n_s, replace=False)
index_7 = np.random.choice(np.where(data_y == 7)[0], size=n_s, replace=False)

threes = data_x[index_3]
sevens = data_x[index_7]

for i in range(to_print):
    io.imsave(f"tmp/three_{i}.png", threes[i].reshape(28, 28))
    io.imsave(f"tmp/seven_{i}.png", sevens[i].reshape(28, 28))


np.save("threes.npy", threes)
np.save("sevens.npy", sevens)
