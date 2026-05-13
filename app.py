# app.py

```python
import streamlit as st
from PIL import Image
import cv2
import numpy as np
from fpdf import FPDF
import tempfile
import os

st.set_page_config(page_title="Document Scanner", layout="centered")

st.title("📄 Document Scanner")
st.write("Upload a document image, convert it to black & white like Adobe Scan, and download it as a PDF.")

uploaded_file = st.file_uploader(
    "Upload a document image",
    type=["jpg", "jpeg", "png"]
)


def process_document(image):
    # Convert PIL image to OpenCV format
    image_np = np.array(image)

    # Convert RGB to BGR for OpenCV
    image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    # Convert to grayscale
    gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)

    # Apply adaptive threshold for scan effect
    scanned = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    return scanned


if uploaded_file is not None:
    # Open uploaded image
    image = Image.open(uploaded_file).convert("RGB")

    st.subheader("Original Image")
    st.image(image, use_container_width=True)

    if st.button("Convert to Scanned PDF"):
        # Process image
        scanned_image = process_document(image)

        st.subheader("Scanned Black & White Image")
        st.image(scanned_image, channels="GRAY", use_container_width=True)

        # Save processed image temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_img:
            temp_image_path = temp_img.name
            cv2.imwrite(temp_image_path, scanned_image)

        # Create PDF
        pdf = FPDF()
        pdf.add_page()

        # PDF page dimensions
        page_width = 190

        # Add image to PDF
        pdf.image(temp_image_path, x=10, y=10, w=page_width)

        # Save PDF temporarily
        pdf_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
        pdf.output(pdf_path)

        # Download button
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="⬇ Download PDF",
                data=pdf_file,
                file_name="scanned_document.pdf",
                mime="application/pdf"
            )

        # Cleanup temp image
        os.remove(temp_image_path)

```

---

# requirements.txt

```txt
streamlit
opencv-python-headless
numpy
Pillow
fpdf
```

---

# Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

# Deploy on GitHub + Streamlit Cloud

1. Push `app.py` and `requirements.txt` to a GitHub repository.
2. Go to:

   * [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect your GitHub account.
4. Select the repository.
5. Deploy the app.

