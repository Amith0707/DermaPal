import torch
import torch.nn.functional as F
import numpy as np
import cv2
from PIL import Image
import torchvision.transforms as T
import uuid
import os

from ai.model_loader import load_dermapal_model
from ai.gradcam import GradCAM



# Heatmap save directory

HEATMAP_DIR = "gradio_app/heatmaps"
os.makedirs(HEATMAP_DIR, exist_ok=True)


# Preprocessing Transform 
def get_transform(model_name):
    if model_name == "inception_v3":
        size = 299
    else:
        size = 224
    
    return T.Compose([
        T.Resize((size, size)),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225])
    ])


# Heatmap Overlay
def overlay_heatmap(cam, img_pil):
    cam = cv2.resize(cam, (img_pil.width, img_pil.height))
    cam = np.uint8(255 * cam)
    cam = cv2.applyColorMap(cam, cv2.COLORMAP_JET)

    img_np = np.array(img_pil)
    blended = cv2.addWeighted(cam, 0.5, img_np, 0.5, 0)
    return blended


#         MAIN INFERENCE FUNCTION USED BY GRADIO
def run_calibrated_inference(model_name, weight_path, pil_image, device="cpu"):

    # Load model + hook layer
    model, target_layer = load_dermapal_model(model_name, weight_path, device)
    cam_extractor = GradCAM(model, target_layer)

    # Preprocess
    transform = get_transform(model_name)
    input_tensor = transform(pil_image).unsqueeze(0).to(device)

    conf_list = []
    heatmaps = []

    # Five-pass calibrated inference
    for _ in range(5):
        logits = model(input_tensor)
        probs = F.softmax(logits, dim=1)

        best_conf, pred_class = probs.max(dim=1)
        conf_list.append(best_conf.item())

        heatmap = cam_extractor.generate(input_tensor, pred_class)
        heatmaps.append(heatmap)

    # Choose the run with highest confidence
    best_idx = int(np.argmax(conf_list))
    best_heatmap = heatmaps[best_idx]
    best_confidence = conf_list[best_idx]

    # Create final heatmap image
    final_heatmap_image = overlay_heatmap(best_heatmap, pil_image)

    # Save heatmap to disk
    filename = f"heatmap_{uuid.uuid4().hex}.png"
    save_path = os.path.join(HEATMAP_DIR, filename)

    # Convert RGB → BGR for OpenCV
    cv2.imwrite(save_path, final_heatmap_image[:, :, ::-1])

    
        # Return inference results
    import time

    # after cv2.imwrite()
    time.sleep(0.02)   # <-- IMPORTANT FIX (lets Windows unlock file)

    return {
        "prediction": pred_class.item(),
        "best_confidence": best_confidence,
        "mean_confidence": float(np.mean(conf_list)),
        "variance": float(np.var(conf_list)),
        "std_dev": float(np.std(conf_list)),
        "heatmap_file": save_path  # renamed for clarity
    }


