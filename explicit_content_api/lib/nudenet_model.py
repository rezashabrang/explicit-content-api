"""Using NudeNet model for classifying images"""
import cv2
from pathlib import Path
from nudenet import NudeClassifierLite
from explicit_content_api.lib.image_utils import load_images
import numpy as np


class ModifiedLiteClassifier(NudeClassifierLite):
    """Modified LiteClassifer for loading image & Reading image"""
    def __init__(self):
        # Getting model path
        model_path = f"{Path(__file__).parent}/models/classifier_lite.onnx"
        self.lite_model = cv2.dnn.readNet(model_path)
    
    def classify(self, image_path, size=(256, 256)):
        result = {}
        loaded_images, _ = load_images([image_path], size, image_names=[image_path])
        loaded_images = np.rollaxis(loaded_images, 3, 1)

        self.lite_model.setInput(loaded_images)
        pred = self.lite_model.forward()
        pred = list(pred)
        result = {
            "unsafe": float(pred[0][0]),
            "safe": float(pred[0][1]),
        }
        return result


def classify_image(image,): 
    """"Classifying image"""
    classifier = ModifiedLiteClassifier()
    res = classifier.classify(image)
    print(res)
    return res