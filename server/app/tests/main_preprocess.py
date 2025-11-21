# server/app/tests/main_preprocess.py

import os
import random
from tqdm import tqdm

from app.logger import setup_logger
from app.tests.io_utils import (
    list_class_folders, 
    make_output_dirs, 
    gather_image_paths, 
    sample_paths,
    save_image_rgb
)
from app.tests.pipeline import process_single_image

def run_preprocessing(
    input_root: str = "dataset/Train",
    output_root: str = "artifacts/processed_images",
    max_per_class: int = 100,
    seed: int = 42,
):
    """
    Runs the entire preprocessing pipeline for all classes.
    - Discovers class folders automatically
    - then it runs the preprocessing pipeline in pipeline.py
    - Saves final PNGs to output_root
    """

    logger = setup_logger("DermaPal_Preprocess")

    input_root = os.path.abspath(input_root)
    output_root = os.path.abspath(output_root)

    logger.info(f"Input root:  {input_root}")
    logger.info(f"Output root: {output_root}")
    logger.info(f"Max per class: {max_per_class}")

    if not os.path.exists(input_root):
        logger.error(f"Input root does not exist: {input_root}")
        raise FileNotFoundError(f"Input folder not found: {input_root}")

    # Discover class folders
    classes = list_class_folders(input_root, logger=logger)
    logger.info(f"Found classes: {classes}")

    # Create output directories
    make_output_dirs(output_root, classes, logger=logger)

    # Set seed for reproducibility
    random.seed(seed)

    # Preprocessing params
    denoise_params = {"d": 9, "sigmaColor": 75, "sigmaSpace": 75}
    clahe_params  = {"clip_limit": 2.0, "tile_grid_size": (8, 8)}

    # Collect samples
    samples_per_class = {}
    total_to_process = 0

    for cls in classes:
        class_dir = os.path.join(input_root, cls)
        all_paths = gather_image_paths(class_dir)

        selected = sample_paths(
            all_paths,
            max_samples=max_per_class,
            seed=seed
        )

        samples_per_class[cls] = selected
        total_to_process += len(selected)

        logger.info(
            f"[{cls}] Total images: {len(all_paths)} | Selected: {len(selected)}"
        )

    logger.info(f"Total images to process: {total_to_process}")

    # Process images
    pbar = tqdm(total=total_to_process, desc="Processing images", unit="img")
    processed_count = 0

    for cls, paths in samples_per_class.items():
        out_class_dir = os.path.join(output_root, cls)

        for in_path in paths:
            try:
                # Create output filename (.png)
                base = os.path.basename(in_path)
                out_name = os.path.splitext(base)[0] + ".png"
                out_path = os.path.join(out_class_dir, out_name)

                # Run pipeline
                final_img = process_single_image(
                    in_path,
                    denoise_params=denoise_params,
                    clahe_params=clahe_params,
                    logger=logger
                )

                save_image_rgb(out_path, final_img, logger=logger)

                processed_count += 1
                pbar.update(1)

            except Exception as e:
                logger.error(f"Failed to process {in_path}: {str(e)}")
                pbar.update(1)

    pbar.close()
    logger.info(f"Processing complete. Processed: {processed_count} images")

def main(): # will be removed during infrenecing via streamlit for now it's CLI(optional)
    run_preprocessing(
        input_root="dataset/Train",
        output_root="artifacts/processed_images",
        max_per_class=100,
        seed=42,
    )

if __name__ == "__main__":
    main()
