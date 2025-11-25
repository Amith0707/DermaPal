"""
Docstring for ai.model_loader

This script is mainly to load the latest pre-trained model
from weights folder
"""
import torch
import torch.nn as nn
from torchvision.models import efficientnet_b0,EfficientNet_B0_Weights
def load_dermapal_model(model_path:str,device="cpu"):
    """
    Docstring for load_dermapal_model
    
    :param model_path: A string to load the pre-trained model
    :type model_path: str
    :param device: To set a device agnostic code

    Note: even though the last layer of pre-trained
    """
    model=efficientnet_b0(weights=None) # to load our model weights
    # Recreate classifier architecture
    model.classifier = nn.Sequential(
        nn.Dropout(0.2, inplace=True),
        nn.Linear(1280, 7)
    )
    state_dict=torch.load(model_path,map_location=device) # overwritinhg
    model.load_state_dict(state_dict)
    model.eval()
    model.to(device)
    print("="*100)
    print("Model loaded successfully..")
    print("="*100)
    return model