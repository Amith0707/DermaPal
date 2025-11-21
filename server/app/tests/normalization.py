# server/app/tests/normalization.py
import cv2
import numpy as np
from typing import Optional, Tuple
from logging import Logger

def clahe_lab(img: np.ndarray, clip_limit: float = 2.0, tile_grid_size: Tuple[int,int] = (8,8),
              logger: Optional[Logger] = None) -> np.ndarray:
    """
    Apply CLAHE on the L channel of LAB color space only.
    Removed GrayWorld since the lesion was not being captured well
    """
    if logger:
        logger.debug("clahe_lab: start")
    if img is None:
        raise ValueError("Input image is None")

    # Convert RGB -> LAB
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    # CLAHE on L channel
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    l_clahe = clahe.apply(l)

    lab_clahe = cv2.merge((l_clahe, a, b))
    bgr_clahe = cv2.cvtColor(lab_clahe, cv2.COLOR_LAB2BGR)
    img_clahe_rgb = cv2.cvtColor(bgr_clahe, cv2.COLOR_BGR2RGB)

    if logger:
        logger.debug("clahe_lab: done")
    return img_clahe_rgb
