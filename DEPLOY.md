# 🚀 Deployment Guide

This guide covers how to deploy the **Context-Aware AI Eraser** to **Heroku**, **Render**, **PythonAnywhere**, and how to share it instantly via **Ngrok**.

---

## ✅ Prerequisites

Ensure you have the following installed:
- [Git](https://git-scm.com/)
- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) (if deploying to Heroku)
- A [GitHub](https://github.com/) account (recommended for easy deployment)

---

## ☁️ Option 1: Deploy to Heroku (Recommended)

Heroku is the easiest way to get this app running.

### 1. Login to Heroku
Open your terminal and run:
```bash
heroku login
```

### 2. Create a New App
Create a new app on Heroku:
```bash
heroku create your-app-name-here
# Example: heroku create context-ai-eraser
```

### 3. Add Buildpacks
This project uses Python and OpenCV. Heroku needs to know this.
```bash
heroku buildpacks:add heroku/python
heroku buildpacks:add https://github.com/heroku/heroku-buildpack-apt
```
*Note: The apt buildpack is often needed for OpenCV system dependencies like `libgl1`.*

### 4. Deploy Code
Push your code to Heroku:
```bash
git push heroku main
```
*(If your branch is `master`, use `git push heroku master`)*

### 5. Scale Dynos
Ensure the web worker is running:
```bash
heroku ps:scale web=1
```

### 6. Open App
```bash
heroku open
```

---

## 🔷 Option 2: Deploy to Render

Render is a great modern alternative to Heroku often with a free tier.

1. **Push your code to GitHub**.
2. Go to [dashboard.render.com](https://dashboard.render.com/).
3. Click **New +** -> **Web Service**.
4. Connect your GitHub repository.
5. **Configure Settings**:
   - **Name**: `context-aware-ai-eraser`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn api.app:app`
6. Click **Create Web Service**.

*Note: If you encounter OpenCV errors on Render, you may need to switch to `opencv-python-headless` in `requirements.txt` or ensure system dependencies are installed via a `render-build.sh` script.*

---

## 🐍 Option 3: PythonAnywhere (Web-Based)

Good for those who prefer a web interface over command line.

1. **Sign up** at [pythonanywhere.com](https://www.pythonanywhere.com/).
2. **Open Bash Console**:
   On your Dashboard, click `$ Bash`.
3. **Clone your Code**:
   ```bash
   git clone https://github.com/vishva2410/context-aware-ai-eraser.git
   cd context-aware-ai-eraser
   pip3 install -r requirements.txt --user
   ```
4. **Configure Web App**:
   - Go to the **Web** tab.
   - Click **Add a new web app**.
   - Select **Flask** -> **Python 3.9** (or newer).
   - **Path to source code**: `/Users/vishvatejaguduguntla/context-aware-ai-eraser`
5. **Configure WSGI File**:
   - Click the link to edit the **WSGI configuration file**.
   - Update it to serve your app:
     ```python
     import sys
     path = '/Users/vishvatejaguduguntla/context-aware-ai-eraser'
     if path not in sys.path:
         sys.path.append(path)
     from api.app import app as application
     ```

---

## 🔗 Option 4: Ngrok (Instant Temporary Link)

Best for quickly showing the app to someone without deploying.

1. **Install Ngrok**: [Download here](https://ngrok.com/download).
2. **Start your App Locally**:
   ```bash
   python -m api.app
   ```
   *(Running on port 5000)*
3. **Expose to Web**:
   In a *new terminal window*, run:
   ```bash
   ngrok http 5000
   ```
4. **Copy Link**: Send the `https://....ngrok-free.app` link to anyone!

---

## 💻 Option 5: Run Locally (Production Mode)

To run the app locally as if it were in production (using Gunicorn instead of the Flask dev server):

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run with Gunicorn**:
   ```bash
   gunicorn api.app:app
   ```
   
3. **Access App**:
   Open [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## ⚠️ Troubleshooting

### "ModuleNotFoundError: No module named 'cv2'"
- This usually means OpenCV dependencies are missing on the server.
- **Heroku**: Ensure you added the `heroku-buildpack-apt` (Step 3 above) and create an `Aptfile` in the root directory with `libgl1-mesa-glx` if needed (though usually `opencv-python-headless` is safer for servers).
- **Fix**: Change `opencv-python` to `opencv-python-headless` in `requirements.txt` specifically for server environments if issues persist.

### "App Crashed" (H10 Error)
- Check logs: `heroku logs --tail`
- Ensure `Procfile` exists and contains `web: gunicorn api.app:app`.

---
