# server/app/tests/pipeline.py
import os
import cv2
import numpy as np
from typing import Optional
from logging import Logger

from app.tests.hair_removal import remove_hairs
from app.tests.denoising import denoise_image
from app.tests.normalization import clahe_lab

def process_single_image(path: str,
                         logger: Optional[Logger] = None,
                         denoise_params: dict = None,
                         clahe_params: dict = None) -> np.ndarray:
    """
    Full pipeline applied on a single image path.
    Returns processed RGB numpy array.
    """
    try:
        if logger:
            logger.debug(f"Processing image: {path}")

        # Read image with cv2 (BGR)
        bgr = cv2.imread(path, cv2.IMREAD_COLOR)
        if bgr is None:
            raise IOError(f"Failed to read image: {path}")

        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

        # 1. Hair removal
        cleaned = remove_hairs(rgb, logger=logger)

        # 2. Denoise (bilateral)
        denoise_params = denoise_params or {}
        denoised = denoise_image(cleaned, logger=logger, **denoise_params)

        # 3. CLAHE on L-channel (LAB)
        clahe_params = clahe_params or {}
        normalized = clahe_lab(denoised, logger=logger, **clahe_params)

        if logger:
            logger.debug("Processing complete for image")
        return normalized

    except Exception:
        if logger:
            logger.exception(f"Error processing image: {path}")
        raise
