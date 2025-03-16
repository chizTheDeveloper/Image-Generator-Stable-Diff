# 🚀 Stable Diffusion XL (SDXL) Web App

A simple **text-to-image generator** using **Stable Diffusion XL 1.0**. Runs **locally** on your laptop with **FastAPI and JavaScript** for a seamless web-based experience.

## 🔧 Features
- 🖼 **Text-to-Image**: Generate high-quality images from text prompts.
- ⚡ **Runs Locally**: No API costs—fully offline!
- 🎨 **SDXL 1.0**: Uses **Stable Diffusion XL** for superior image generation.
- 🔌 **FastAPI Backend**: Handles image generation with GPU acceleration.
- 🌐 **HTML + JavaScript Frontend**: Simple web UI for entering prompts.

## 📂 Project Structure summary
📁 project-folder │── 📄 index.html # Web UI (User input form) │── 📄 style.css # Basic styling │── 📄 app.js # JavaScript (Handles API calls) │── 📄 server.py # FastAPI backend (Runs SDXL model) │── 📂 static/ # Stores generated images


## 🚀 Setup & Run
### 1️⃣ Install Dependencies
Ensure **Python, PyTorch, and Diffusers** are installed:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install diffusers transformers accelerate safetensors fastapi uvicorn pillow

##Run program
inputin console: python server.py
open indedx.html on web browser and issue prompt
