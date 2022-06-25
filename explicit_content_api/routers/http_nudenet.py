"""Upscale endpoints"""
from fastapi import APIRouter, HTTPException, UploadFile, Response


# ------------------------------ Initialization -------------------------------
router = APIRouter()
LOGGER = LoggerSetup(__name__, "info").get_minimal()

@router.post(
    "/api/image-classifer/",
    response_model=dict,
    status_code=200
)
async def upscale_image(
    model: str,
    image: UploadFile,
):
    """ **Args**
        * **model:**
        Name of the model.
        """
    try:
        print("")

    except HTTPException as err:
        LOGGER.error(err)
        raise HTTPException(
            status_code=err.status_code,
            detail=err.detail
        ) from err

    except Exception as err:
        LOGGER.error(err)
        raise HTTPException(status_code=400) from err