from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from diffusers import DiffusionPipeline
import torch
import os
import re
import asyncio
import uuid

# Initialize FastAPI
app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for production, specify domains)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load Stable Diffusion model
pipe = DiffusionPipeline.from_pretrained(
    "stabilityai/sdxl-turbo",
    torch_dtype=torch.float16
).to("cuda")

pipe.enable_attention_slicing()  # Reduce memory usage

# Create static folder if not exists
os.makedirs("static", exist_ok=True)


def sanitize_filename(prompt: str) -> str:
    """Sanitize a prompt to create a valid filename."""
    sanitized = re.sub(r"[^a-zA-Z0-9_-]", "-", prompt.lower().strip())
    return sanitized[:50]  # Limit filename length


def get_unique_filename(prompt: str) -> str:
    """Generate a unique filename to prevent overwriting existing images."""
    base_name = sanitize_filename(prompt)
    filename = f"{base_name}.png"

    count = 1
    while os.path.exists(f"static/{filename}"):
        filename = f"{base_name}-{count}.png"
        count += 1

    return filename


@app.post("/generate/")
async def generate_image(request: Request):
    """Generate an image while updating progress via Server-Sent Events."""
    data = await request.json()
    prompt = data.get("prompt", "An AI-generated image")

    # Generate a unique filename
    image_filename = get_unique_filename(prompt)
    image_path = f"static/{image_filename}"

    async def image_generator():
        num_steps = 10  # Number of inference steps
        for i in range(1, num_steps + 1):
            await asyncio.sleep(0.5)  # Simulate processing delay
            yield f"data: {int((i / num_steps) * 90)}\n\n"  # Progress updates up to 90%

        # Generate image
        image = pipe(prompt, num_inference_steps=num_steps, height=512, width=512).images[0]
        image.save(image_path)

        yield f"data: 100, /static/{image_filename}\n\n"  # Final update with image URL

    return StreamingResponse(image_generator(), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
