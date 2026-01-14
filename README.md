# 🛡️ Context-Aware AI Eraser

> **A privacy-focused computer vision system that safeguards sensitive data through hybrid AI detection and human-in-the-loop control.**

![Project Banner](https://via.placeholder.com/1000x300?text=Context+Aware+AI+Eraser+Demo)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green)
![Status](https://img.shields.io/badge/Status-Prototype-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

## 📖 Overview

In the age of social media, accidental "doxxing" (revealing private info) is a major risk. **Context-Aware AI Eraser** is not just a blurring tool; it is an intelligent pipeline that detects sensitive entities (Faces, License Plates, ID Cards) and offers users a "Context Switch."

Unlike fully automated systems that might over-censor or miss details, this project uses a **Hybrid AI + User-Control** design. It identifies potential risks and asks the user: *"Is this Public or Private context?"* to determine the severity of the erasure.

## ✨ Key Features

* **Multi-Class Detection:** Automatically identifies:
    * 👤 **Faces** (using MediaPipe/Haar Cascades)
    * 🚗 **License Plates** (using OCR/YOLO)
    * 💳 **ID-Like Regions** (Credit cards, badges, documents).
* **Context Logic:**
    * **Public Mode:** Minimal redaction (e.g., only blurs license plates, keeps faces visible).
    * **Private Mode:** Aggressive redaction (blurs/erases faces, IDs, and background text).
* **Smart Erasure:** Uses inpainting algorithms to remove objects cleanly rather than just placing a black box.
* **Privacy-First Architecture:** All processing happens locally on the device; no images are sent to the cloud.

## 🛠️ Tech Stack

* **Language:** Python
* **Computer Vision:** OpenCV, MediaPipe
* **UI/Frontend:** Streamlit / Gradio
* **Image Processing:** NumPy, PIL

## 🚀 Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/yourusername/context-aware-ai-eraser.git](https://github.com/yourusername/context-aware-ai-eraser.git)
    cd context-aware-ai-eraser
    ```

2.  **Create a virtual environment (Recommended):**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 💻 Usage

1.  Run the application:
    ```bash
    streamlit run app.py
    # OR if using a script
    python main.py
    ```
2.  **Upload an Image:** Select an image containing sensitive data.
3.  **Select Context:** Toggle between `Public` or `Private` mode.
4.  **Review & Export:** The AI will highlight detected regions. Confirm the erasure and download the sanitized image.

## 🧠 How It Works

1.  **Input:** Image is loaded into the pipeline.
2.  **Detection Layer:** The image passes through multiple detection models.
3.  **Region Proposal:** The system generates bounding boxes for all sensitive content.
4.  **Context Filter:**
    * *If Context == Public:* Ignore Faces, Mask Plates.
    * *If Context == Private:* Mask Faces, Mask Plates, Mask IDs.
5.  **Rendering:** OpenCV applies Gaussian Blur or Inpainting to the selected regions.

## 🔮 Future Roadmap

* [ ] **Automated Transmission Guard:** Develop a middleware/API wrapper that intercepts image uploads (e.g., browser extensions or OS-level hooks) to auto-sanitize files *before* they leave the local device.
* [ ] **Semantic Scene Understanding (ViT/CLIP):** Move beyond simple object detection to "Contextual Understanding" using Vision Transformers. The system will recognize the *scenario* (e.g., "User is holding a passport" vs. "User is holding a book") to trigger auto-redaction.
* [ ] **OCR + NLP PII Extraction:** Integrate Optical Character Recognition with Named Entity Recognition to detect and blur specific text on screens or documents (e.g., Credit Card numbers, passwords, addresses) while leaving safe text visible.
* [ ] **Adversarial Privacy Masks:** Implement noise layers that confuse third-party facial recognition algorithms (scrapers) even if the visual blur is reversed.

## 🤝 Contributing

Contributions are welcome! Please read `CONTRIBUTING.md` for details on our code of conduct, and the process for submitting pull requests.
