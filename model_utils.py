from keras.applications.vgg19 import VGG19
from keras.applications.vgg16 import VGG16
from keras import backend
import numpy as np


def remove_last_layers(model):
    """To remove the last FC layers of VGG and get the 4096 dim features"""
    model.layers.pop()
    model.layers.pop()
    model.outputs = [model.layers[-1].output]
    model.layers[-1].outbound_nodes = []


vgg_model_16 = VGG16(include_top=True, weights="imagenet")
vgg_model_19 = VGG19(include_top=True, weights="imagenet")

remove_last_layers(vgg_model_16)
remove_last_layers(vgg_model_19)

def get_features(image, model_name="vgg16"):

    if backend.image_dim_ordering()=='th':
        print "Please switch to tensorflow backend. Update to reorder will come soon."
        return None

    if model_name.lower() in ["vgg16", "vgg_16"]:
        model = vgg_model_16

    if model_name.lower() in ["vgg19", "vgg_19"]:
        model = vgg_model_19

    imageTensor = np.zeros((1, 224, 224, 3))
    imageTensor[0] = image

    modelFeature =  model.predict(imageTensor)[0]
    return modelFeature


if __name__=="__main__":
    import cv2
    inputImage = cv2.resize(cv2.imread("testImages/test1.jpg"), (224, 224))
    from time import time
    start = time()
    vector = get_features(inputImage, 'vgg19')
    print 'time taken by vgg 19:',time()-start,'seconds. Vector shape:',vector.shape
    start = time()
    vector = get_features(inputImage, 'vgg16')
    print 'time taken by vgg 16:',time()-start,'seconds. Vector shape:',vector.shape
