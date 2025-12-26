"""
Model loader for DermaPal models.
Loads any of the four fine-tuned CNN models using TIMM (the library used during training).
"""

import torch
import timm


TARGET_LAYERS = {
    "efficientnet_b0": "blocks.6",
    "efficientnet_b3": "blocks.6",
    "resnet50": "layer4",
    "inception_v3": "Mixed_7c"
}


def load_dermapal_model(model_name: str, weight_path: str, device: str = "cpu"):
    """
    Loads a model architecture exactly matching the one used during training.
    Uses timm.create_model() for all architectures.
    """

    print(f"[INFO] Loading model architecture: {model_name}")

    model = timm.create_model(model_name, pretrained=False, num_classes=4)

    print(f"[INFO] Loading weights: {weight_path}")
    state_dict = torch.load(weight_path, map_location=device)
    model.load_state_dict(state_dict)

    model.eval()
    model.to(device)

    print("[INFO] Model loaded successfully")

    return model, TARGET_LAYERS[model_name]
