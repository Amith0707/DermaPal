import torch
import numpy as np
import cv2

class GradCAM:
    def __init__(self, model, target_layer):
        self.model = model
        self.model.eval()

        self.gradients = None
        self.activations = None

        layer = dict(model.named_modules())[target_layer]
        layer.register_forward_hook(self._save_activations)
        layer.register_backward_hook(self._save_gradients)

    def _save_activations(self, module, inp, out):
        self.activations = out.detach()

    def _save_gradients(self, module, grad_in, grad_out):
        self.gradients = grad_out[0].detach()

    def generate(self, input_tensor, class_idx):
        output = self.model(input_tensor)
        loss = output[:, class_idx]

        self.model.zero_grad()
        loss.backward(retain_graph=True)

        grads = self.gradients      # [B,C,H,W]
        acts = self.activations     # [B,C,H,W]

        weights = grads.mean(dim=[2, 3], keepdim=True)
        cam = (weights * acts).sum(dim=1).squeeze()

        cam = torch.relu(cam)
        cam -= cam.min()
        cam /= cam.max() + 1e-7

        return cam.cpu().numpy()
