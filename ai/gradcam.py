"""
Docstring for ai.gradcam
"""

import torch
import torch.nn.functional as f
import numpy as np
import cv2

class GradCAM:

    def __init__(self,model,device="cpu"):
        self.model=model
        self.device=device
        
        # Fetching the last Conv layer
        self.target_layer=model.features[7][0].block[1][0]

        # Clearing existing hooks
        self.target_layer._forward_hooks.clear()
        self.target_layer._backward_hooks.clear()
        self.target_layer._forward_pre_hooks.clear()

        # Storing the gradients for GRAD CAM
        self.activations=[]
        self.gradients=[]

        # Registering HOOKS
        self.tar
