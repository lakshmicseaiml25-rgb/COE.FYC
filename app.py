import streamlit as st
from PIL import Image
import cv2
import numpy as np
from fpdf import FPDF
import tempfile
import os

st.set_page_config(page_title="Color Document Scanner", layout="centered")

st.title("📄 Color Document Scanner")
st.write(
    "Upload a document image, apply a red-blue scan effect, convert it to PDF, and download it."
)

uploaded_file = st.file_uploader(
    "Upload a document image",
    type=["jpg", "jpeg", "png"]
)


def process_document(image):
    # Convert PIL image to OpenCV format
    image_np = np.array(image)

    # Convert RGB to BGR
    img = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    # Resize for better processing
    img = cv2.resize(img, None, fx=1.2, fy=1.2)

    # Increase contrast
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)

    enhanced = cv2.merge((cl, a, b))
    enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)

    # Create red-blue effect
    blue_channel = enhanced[:, :, 0]
    red_channel = enhanced[:, :, 2]

    # Enhance channels
    blue_channel = cv2.equalizeHist(blue_channel)
    red_channel = cv2.equalizeHist(red_channel)

    # Create merged effect
    effect = np.zeros_like(enhanced)
    effect[:, :, 0] = blue_channel     # Blue
    effect[:, :, 1] = 40               # Small green tint
    effect[:, :, 2] = red_channel      # Red

    # Sharpen image
    kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ])

    sharp = cv2.filter2D(effect, -1, kernel)

    return sharp


if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")

    st.subheader("Original Image")
    st.image(image, use_container_width=True)

    if st.button("Convert to Styled PDF"):
        processed_image = process_document(image)

        # Convert BGR to RGB for display
        display_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)

        st.subheader("Processed Red-Blue Scan")
        st.image(display_image, use_container_width=True)

        # Save image temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_img:
            temp_image_path = temp_img.name
            cv2.imwrite(temp_image_path, processed_image)

        # Create PDF
        pdf = FPDF()
        pdf.add_page()

        # Fit image on page
        pdf.image(temp_image_path, x=10, y=10, w=190)

        # Save PDF temporarily
        pdf_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
        pdf.output(pdf_path)

        # Download button
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="⬇ Download PDF",
                data=pdf_file,
                file_name="styled_document.pdf",
                mime="application/pdf"
            )

        # Cleanup
        os.remove(temp_image_path)
