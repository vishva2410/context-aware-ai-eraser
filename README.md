# 🛡️ Context-Aware AI Eraser

> **A privacy-focused computer vision system that detects and anonymizes sensitive visual content using a hybrid AI + user-controlled design.**

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Computer Vision](https://img.shields.io/badge/Computer%20Vision-OpenCV-green)
![YOLO](https://img.shields.io/badge/YOLOv8-Object%20Detection-orange)
![Status](https://img.shields.io/badge/Status-Prototype-yellow)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 📖 Overview

Accidental exposure of sensitive visual information (faces, license plates, IDs) is a growing privacy risk in the age of social media and digital sharing.

**Context-Aware AI Eraser** is a **privacy-first image processing system** that detects sensitive regions in images and anonymizes them based on **user intent**, rather than relying on fully automatic deletion.

Instead of blindly blurring everything, the system follows a **hybrid AI + human-in-the-loop approach**:
- AI detects *potentially sensitive regions*
- The user decides *how aggressively* those regions should be anonymized

This mirrors how real-world privacy tools are designed.

---

## 🎯 Core Design Philosophy

**Context ≠ Metadata**  
Context = **User Intent**

The system is built around two modes:

- **Public Context**
  - Minimal anonymization
  - Preserve usability and aesthetics
- **Private Context**
  - Aggressive anonymization
  - Maximum privacy protection

This avoids over-censorship while still protecting sensitive data.

---

## ✨ Key Features (Current)

- **Face Detection**
  - YOLOv8-based face detector
  - Trained on the WIDER FACE dataset
  - Bounding-box based detection
- **Modular Backend Architecture**
  - Separate detectors per object type
  - Pipeline-based design for extensibility
- **Privacy-Oriented Anonymization**
  - Face blurring using OpenCV
- **Local Processing**
  - No cloud dependency
  - Images processed entirely on-device

---

## 🧪 Project Status

### ✅ Implemented
- YOLOv8 face detection model
- Flask backend API
- Modular detection pipeline
- End-to-end image upload → detection → anonymization (prototype)

### 🚧 In Progress
- Blur pipeline stabilization
- Context-based anonymization rules
- API response standardization

### 🗓️ Planned
- License plate detection
- ID / document region detection
- Erase (inpainting) mode for private context
- Simple frontend UI for context selection

---

## 🛠️ Tech Stack

- **Language:** Python 3.9+
- **Backend:** Flask
- **Computer Vision:** OpenCV
- **Object Detection:** YOLOv8 (Ultralytics)
- **Image Processing:** NumPy, Pillow

---

## 🚀 Installation (Development)

```bash
git clone https://github.com/vishva2410/context-aware-ai-eraser.git
cd context-aware-ai-eraser

python3 -m venv venv
source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate    # Windows

pip install -r requirements.txt
````

---

## ▶️ Running the Backend

```bash
python -m api.app
```

Then open:

```
http://127.0.0.1:5000
```

---

## 🧠 High-Level Workflow

1. Image is uploaded to the backend
2. Detection pipeline identifies sensitive regions
3. Bounding boxes are generated
4. Anonymization logic applies blur based on context
5. Sanitized image is returned

---

## 🔮 Future Roadmap

* License plate detection using YOLO
* ID-like region detection (documents, badges)
* Inpainting-based erase mode
* Frontend for interactive context selection
* Improved scene understanding for smarter redaction

---

## 📌 Disclaimer

This project is an **academic / prototype system** and is not intended for production deployment without further validation, optimization, and security hardening.

---

## 📜 License

This project is licensed under the **MIT License**.

````

---

## ✅ What to do next (important)

1. Paste this into `README.md`
2. Commit:
   ```bash
   git add README.md
   git commit -m "Improve README: clarify scope, architecture, and project status"
````

3. Push after rebase (as discussed earlier)

---
