# 🛡️ Context-Aware AI Eraser

> **A privacy-focused computer vision system that detects and anonymizes sensitive visual content (Faces, License Plates, ID Cards) using a hybrid AI + user-controlled design.**

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Computer Vision](https://img.shields.io/badge/Computer%20Vision-OpenCV-green)
![YOLO](https://img.shields.io/badge/YOLOv8-Object%20Detection-orange)
![Frontend](https://img.shields.io/badge/Frontend-HTML%2FCSS%2FJS-purple)
![Status](https://img.shields.io/badge/Status-Beta-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 📖 Overview

Accidental exposure of sensitive visual information (faces, license plates, IDs) is a growing privacy risk in the age of social media and digital sharing.

**Context-Aware AI Eraser** is a **privacy-first image processing system** that detects sensitive regions in images and anonymizes them based on **user intent**, rather than relying on fully automatic deletion.

Instead of blindly blurring everything, the system follows a **hybrid AI + human-in-the-loop approach**:
- AI detects *potentially sensitive regions*
- The user decides *how aggressively* those regions should be anonymized via a comprehensive UI.

---

## 🎯 Core Design Philosophy

**Context ≠ Metadata**  
Context = **User Intent**

The system is built around two modes:

- **Public Context**
  - Minimal anonymization (Blurring)
  - Preserve usability and aesthetics
- **Private Context**
  - Aggressive anonymization (Inpainting/Blackout)
  - Maximum privacy protection

---

## ✨ Key Features

- **Multi-Object Detection**
  - **Faces**: YOLOv8-based face detector (WIDER FACE)
  - **License Plates**: Specialized License Plate detector
  - **ID Cards**: **[NEW]** Document and ID card detection
- **Premium Web Interface**
  - Modern, Glassmorphism-inspired UI
  - Real-time Public/Private context switching
  - Drag-and-drop file upload
- **Modular Backend Architecture**
  - Separate detectors per object type
  - Pipeline-based design for extensibility
  - Flask API with static file serving
- **Local Processing**
  - No cloud dependency
  - Images processed entirely on-device

---

## 🧪 Project Status

### ✅ Implemented
- **YOLOv8 Object Detection**: Faces, License Plates, ID Cards.
- **Privacy Pipeline**: Configurable contexts (Public/Private).
- **Frontend**: Beautified HTML/CSS/JS interface.
- **Backend**: Robust Flask API handling uploads and processing.

### 🗓️ Planned
- Advanced Scene Understanding (ViT/CLIP)
- Video Processing Support

---

## 🛠️ Tech Stack

- **Language:** Python 3.9+
- **Backend:** Flask
- **Frontend:** HTML5, CSS3, Vanilla JS
- **Computer Vision:** OpenCV
- **Object Detection:** YOLOv8 (Ultralytics)
- **Image Processing:** NumPy, Pillow

---

## 🚀 Installation

```bash
git clone https://github.com/vishva2410/context-aware-ai-eraser.git
cd context-aware-ai-eraser

python3 -m venv venv
source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate    # Windows

pip install -r requirements.txt
````

---

## ▶️ Running the Application

1. **Start the Backend**:
   ```bash
   python -m api.app
   ```

2. **Access the Interface**:
   Open browser to:
   ```
   http://127.0.0.1:5000
   ```

---

## 🧠 High-Level Workflow

1. Image is uploaded via the Web UI.
2. User selects **Context** (Public vs Private).
3. Detection pipeline identifies sensitive regions (Faces, Plates, IDs).
4. Anonymization logic applies blur or erase based on context.
5. Protected image is displayed instantly.

---

## 📜 License

This project is licensed under the **MIT License**.
