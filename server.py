from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from diffusers import DiffusionPipeline
import torch
from PIL import Image
import uuid
import os
import asyncio

# Initialize FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for production, specify allowed domains)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)
# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load Stable Diffusion model
pipe = DiffusionPipeline.from_pretrained(
    "stabilityai/sdxl-turbo",
    torch_dtype=torch.float16
).to("cuda")

pipe.enable_attention_slicing()  # Reduces memory usage


# Create a folder to store images if it doesn’t exist
os.makedirs("static", exist_ok=True)

@app.post("/generate/")
async def generate_image(request: Request):
    """Generate image and stream progress to frontend"""
    data = await request.json()
    prompt = data.get("prompt", "An AI-generated image")
    image_filename = f"static/{uuid.uuid4().hex}.png"

    async def image_generator():
        for i in range(1, 11):  # Simulate 10 progress steps
            await asyncio.sleep(0.5)  # Simulate processing delay
            yield f"data: {i * 10}\n\n"  # Send progress percentage
        
        # Generate image
        image = pipe(prompt, num_inference_steps=10, height=512, width=512).images[0]
        image.save(image_filename)

        # Send final update
        yield f"data: 100, {image_filename}\n\n"

    return StreamingResponse(image_generator(), media_type="text/event-stream")

@app.get("/latest-image/")
async def get_latest_image():
    """Retrieve the most recently generated image from the static folder."""
    static_dir = "static"
    images = [f for f in os.listdir(static_dir) if f.endswith((".png", ".jpg", ".jpeg"))]

    if not images:
        return JSONResponse(content={"error": "No images found"}, status_code=404)

    latest_image = max(images, key=lambda img: os.path.getctime(os.path.join(static_dir, img)))
    return {"image_url": f"/static/{latest_image}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)