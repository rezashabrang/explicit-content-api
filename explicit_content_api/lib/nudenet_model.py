"""Using NudeNet model for classifying images"""
from typing import Any, Dict

from pathlib import Path

import cv2
import numpy as np

from explicit_content_api.lib.image_utils import load_images


class ModifiedLiteClassifier:
    """Modified LiteClassifer for loading image & Reading image"""

    def __init__(self):
        # Getting model path
        model_path = f"{Path(__file__).parent}/models/classifier_lite.onnx"
        self.lite_model = cv2.dnn.readNet(model_path)

    def classify(self, image_path, size=(256, 256)):
        """Classifying image"""
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


def classify_image(
    image: Any,
) -> Dict[str, float]:
    """ "Classifying image"""
    classifier = ModifiedLiteClassifier()
    res: Dict[str, float] = classifier.classify(image)
    print(res)
    return res
