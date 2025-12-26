import gradio as gr
import os
from PIL import Image

from ai.inference_pipeline import run_calibrated_inference
from server.app.tests.pipeline import process_single_image


MODEL_DIR = "ai/weights"

MODEL_PATHS = {
    "EfficientNet-B0": f"{MODEL_DIR}/efficientnet_b0_best.pth",
    "EfficientNet-B3": f"{MODEL_DIR}/efficientnet_b3_best.pth",
    "ResNet-50":       f"{MODEL_DIR}/resnet50_best.pth",
    "Inception-V3":    f"{MODEL_DIR}/inception_v3_best.pth",
}

MODEL_NAME_MAP = {
    "EfficientNet-B0": "efficientnet_b0",
    "EfficientNet-B3": "efficientnet_b3",
    "ResNet-50":       "resnet50",
    "Inception-V3":    "inception_v3",
}


# Preprocessing
def preprocess_image(img_path):
    print("[INFO] Starting preprocessing")
    print(f"[DEBUG] Raw image path: {img_path}")

    processed_rgb = process_single_image(img_path)
    if processed_rgb is None:
        print("[ERROR] Preprocessing failed")
        raise RuntimeError("Preprocessing pipeline failed")

    print("[INFO] Preprocessing done")
    return Image.fromarray(processed_rgb)


# Inference
def run_inference(model_choice, raw_image_path):

    print(f"[INFO] Inference started for: {model_choice}")
    print(f"[DEBUG] Uploaded path: {raw_image_path}")

    if raw_image_path is None:
        return "No image uploaded", None, None, None

    model_key = MODEL_NAME_MAP[model_choice]
    weight_path = MODEL_PATHS[model_choice]

    print(f"[INFO] Using weights: {weight_path}")

    # Step 1: Preprocess
    try:
        preprocessed_pil = preprocess_image(raw_image_path)
    except Exception as e:
        print(f"[ERROR] Preprocessing error: {e}")
        return f"Preprocessing failed: {e}", None, None, None

    # Step 2: Inference
    print("[INFO] Running calibrated inference...")
    try:
        outputs = run_calibrated_inference(
            model_name=model_key,
            weight_path=weight_path,
            pil_image=preprocessed_pil,
            device="cpu"
        )
    except Exception as e:
        print(f"[ERROR] Inference error: {e}")
        return f"Inference failed: {e}", None, None, None

    print("[INFO] Inference completed")

    prediction = outputs["prediction"]
    best_conf = outputs["best_confidence"]
    mean_conf = outputs["mean_confidence"]
    variance = outputs["variance"]
    heatmap_file = outputs["heatmap_file"]    # <<—— FIXED

    # print(f"[INFO] Heatmap saved at: {heatmap_path}")
    CLASS_LABELS = {
        0: "Melanoma",
        1: "Nevus",
        2: "Basal Cell Carcinoma",
        3: "Benign Keratosis"
    }

    return (
        f"Predicted Class: {CLASS_LABELS[prediction]}",
        f"Best Confidence: {best_conf:.4f}",
        f"Mean: {mean_conf:.4f} | Variance: {variance:.6f}",
        heatmap_file
    )


# Gradio UI
interface = gr.Interface(
    fn=run_inference,
    inputs=[
        gr.Dropdown(
            choices=list(MODEL_PATHS.keys()),
            value="EfficientNet-B0",
            label="Select Model"
        ),
        gr.Image(type="filepath", label="Upload Skin Image")
    ],
    outputs=[
        gr.Textbox(label="Prediction"),
        gr.Textbox(label="Confidence (Best)"),
        gr.Textbox(label="Mean & Variance"),
        gr.Image(label="Grad-CAM Heatmap")
    ],
    title="DermaPal – Explainable Skin Disease Classifier",
    description="Hair removal → Denoise → CLAHE → Prediction → Grad-CAM."
)

if __name__ == "__main__":
    interface.launch()
