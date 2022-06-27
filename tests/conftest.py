import os
import pytest
from pathlib import Path

@pytest.fixture(scope="function")
def load_test_images():
    """Loading two test images"""
    images_folder = f"{Path(__file__).parent}/test_image/"
    image_names = os.listdir(images_folder)
    images = []  # Initializing images
    for image in image_names:
        img_path = images_folder + image
        with open(img_path, "rb") as image_file:
            files = {"image": image_file.read(), "type":"image/png"}
            images.append(files)
    
    return images

