import os
import torch
from PIL import Image

from ai.model_loader import load_dermapal_model

DEVICE="cuda" if torch.cuda.is_available() else "cpu"
MODEL_PATH=os.path.join(
    os.path.dirname(__file__), # gets curr working directory
    "weights",
    "efficientnet_b0_dermapal.pth"
)

print("="*100)
print(f"[DERMAPAL AI] Loading the model from: {MODEL_PATH}")

# Loading the model
model=load_dermapal_model(MODEL_PATH,device=DEVICE)

# intialzing the grad-cam
 