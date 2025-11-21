# server/app/tests/denoising.py
import cv2
import numpy as np
from typing import Optional
from logging import Logger

def denoise_image(img: np.ndarray, d: int = 9, sigmaColor: int = 75, sigmaSpace: int = 75,
                  logger: Optional[Logger] = None) -> np.ndarray:
    """
    Apply bilateral filter to an RGB image.
    The filter preserves edges while smoothing flat regions.
    Best found parms for this was 9:d sigmaColor as 75 and sigmaSpace as 75 as well
    """
    if logger:
        logger.debug("denoise_image: start")
    if img is None:
        raise ValueError("Input image is None")

    # OpenCV bilateralFilter expects BGR, apply to RGB by converting first
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    denoised_bgr = cv2.bilateralFilter(img_bgr, d=d, sigmaColor=sigmaColor, sigmaSpace=sigmaSpace)
    denoised = cv2.cvtColor(denoised_bgr, cv2.COLOR_BGR2RGB)

    if logger:
        logger.debug("denoise_image: done")
    return denoised
