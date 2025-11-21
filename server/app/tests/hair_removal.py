# server/app/tests/hair_removal.py
import cv2
import numpy as np
from typing import Optional
from logging import Logger

def remove_hairs(img: np.ndarray, logger: Optional[Logger] = None) -> np.ndarray:
    """
    Remove hairs from a single RGB image using blackhat + inpaint.
    """
    if logger:
        logger.debug("remove_hairs: start")
    if img is None:
        raise ValueError("Input image is None")

    if img.ndim == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)# Convert to gray for morphology

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel)

    # Threshold the blackhat to create mask of hairs
    _, mask = cv2.threshold(blackhat, 10, 255, cv2.THRESH_BINARY)

    # Inpaint using TELEA algorithm
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    inpainted = cv2.inpaint(img_bgr, mask, inpaintRadius=1, flags=cv2.INPAINT_TELEA)
    img_inpaint = cv2.cvtColor(inpainted, cv2.COLOR_BGR2RGB)

    if logger:
        logger.debug("remove_hairs: done")
    return img_inpaint
