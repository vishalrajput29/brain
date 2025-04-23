import streamlit as st
from ultralytics import YOLO
import gdown
import os
from PIL import Image
import io

# Google Drive file info
GDRIVE_FILE_ID = "1nFgDiO15zwI8Z6fKujd4xRNMGh_XliK5"
MODEL_FILENAME = "best.pt"

# Step 1: Download model from Google Drive if not already present
def download_model_from_gdrive():
    if not os.path.exists(MODEL_FILENAME):
        url = f"https://drive.google.com/uc?id={GDRIVE_FILE_ID}"
        with st.spinner("📥 Downloading model from Google Drive..."):
            gdown.download(url, MODEL_FILENAME, quiet=False)
        st.success("✅ Model downloaded successfully.")

# Step 2: Download and load the model
download_model_from_gdrive()
model = YOLO(MODEL_FILENAME)

# Streamlit UI
st.title("🧠 Brain Tumor Detection")
st.write("Upload an MRI image and the model will detect possible tumors.")

uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Load and display uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Run detection
    with st.spinner("🔍 Running object detection..."):
        results = model(image)
        result = results[0]
        result_image = result.plot()

    # Convert to PIL and display result
    result_image_pil = Image.fromarray(result_image)
    st.image(result_image_pil, caption="Detection Result", use_column_width=True)

    # Optional: Download button for result
    output = io.BytesIO()
    result_image_pil.save(output, format="JPEG")
    st.download_button("📥 Download Result", data=output.getvalue(), file_name="detection_result.jpg", mime="image/jpeg")
