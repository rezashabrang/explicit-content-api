"""Upscale endpoints"""
from fastapi import APIRouter, HTTPException, UploadFile, Response
from explicit_content_api.logger import LoggerSetup
from explicit_content_api.lib.nudenet_model import classify_image
import cv2
import numpy as np
from time import time

# ------------------------------ Initialization -------------------------------
router = APIRouter()
LOGGER = LoggerSetup(__name__, "info").get_minimal()

@router.post(
    "/api/image-classifer/",
    response_model=dict,
    status_code=200
)
async def classify_image(
    image: UploadFile,
):
    """Upload image.
    """
    try:
        s_tot = time()
        # Preprocessing the image
        contents = await image.read()
        nparr = np.fromstring(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        # Classifier
        res = classify_image(image)
        e_tot = time()

        print(f"TOTAL TIME {(e_tot - s_tot) * 1000} ms")
        return res

    except HTTPException as err:
        LOGGER.error(err)
        raise HTTPException(
            status_code=err.status_code,
            detail=err.detail
        ) from err

    except Exception as err:
        LOGGER.error(err)
        raise HTTPException(status_code=400) from err