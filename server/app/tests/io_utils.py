# for fetching images and how many are there
import os
import cv2
import random
from typing import List, Tuple
from logging import Logger

def list_class_folders(root_dir: str, logger: Logger = None) -> List[str]:
    """
    List immediate subdirectories (class folders) in root_dir.
    """
    if logger:
        logger.info(f"Scanning for class folders in: {root_dir}")
    names = []
    for entry in sorted(os.listdir(root_dir)):
        path = os.path.join(root_dir, entry)
        if os.path.isdir(path):
            names.append(entry)
    if logger:
        logger.info(f"Found {len(names)} class folders.")
    return names

def make_output_dirs(output_root: str, class_names: List[str], logger: Logger = None) -> None:
    """
    Create output_root and class subfolders. Overwrites are allowed at file level.
    """
    os.makedirs(output_root, exist_ok=True)
    for cname in class_names:
        out = os.path.join(output_root, cname)
        os.makedirs(out, exist_ok=True)
        if logger:
            logger.debug(f"Created/checked output folder: {out}")

def gather_image_paths(class_dir: str) -> List[str]:
    """
    Return full paths of files inside a class_dir (non-recursive).
    """
    fns = [os.path.join(class_dir, f) for f in sorted(os.listdir(class_dir))
           if os.path.isfile(os.path.join(class_dir, f))]
    return fns

def sample_paths(paths: List[str], max_samples: int = 100, seed: int = 42) -> List[str]:
    """
    Randomly sample up to max_samples from paths. If fewer than max_samples are available,
    return all.
    """
    if len(paths) <= max_samples:
        return list(paths)
    rnd = random.Random(seed)
    return rnd.sample(paths, max_samples)

def save_image_rgb(path: str, img_rgb, logger: Logger = None) -> None:
    """
    Save an RGB image as PNG using cv2.imwrite (convert to BGR first).
    Overwrites existing file.
    """
    out_dir = os.path.dirname(path)
    os.makedirs(out_dir, exist_ok=True)
    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    # Force PNG by ensuring extension .png
    if not path.lower().endswith(".png"):
        path = os.path.splitext(path)[0] + ".png"
    success = cv2.imwrite(path, img_bgr)
    if logger:
        if success:
            logger.debug(f"Saved image: {path}")
        else:
            logger.error(f"Failed to save image: {path}")
