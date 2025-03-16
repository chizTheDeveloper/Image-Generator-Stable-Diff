from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from diffusers import DiffusionPipeline
import torch
import uuid
import os

# Create static directory if it doesn't exist
os.makedirs("static", exist_ok=True)

# Initialize FastAPI
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load Stable Diffusion XL model
pipe = DiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16
).to("cuda")

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate/")
async def generate_image(request: PromptRequest):
    image = pipe(request.prompt).images[0]
    
    # Save image
    image_filename = f"output_{uuid.uuid4().hex}.png"
    image_path = f"static/{image_filename}"
    image.save(image_path)

    return {"image_url": image_path}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)