"""
ThumbnailAI - FastAPI Backend
AI-powered YouTube thumbnail generation with face consistency
"""

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
import replicate
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="ThumbnailAI API",
    description="AI-powered YouTube thumbnail generation",
    version="1.0.0"
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://thumbnailai.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Replicate API setup
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
if not REPLICATE_API_TOKEN:
    print("WARNING: REPLICATE_API_TOKEN not set")
else:
    os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN


# ============== Models ==============

class ThumbnailRequest(BaseModel):
    """Request model for thumbnail generation"""
    prompt: str = Field(..., description="Description of the thumbnail")
    style: Optional[str] = Field("youtube", description="Style template")
    face_image_url: Optional[str] = Field(None, description="URL of face for consistency")
    text_overlay: Optional[str] = Field(None, description="Text to overlay")
    resolution: Optional[str] = Field("1080p", description="720p, 1080p, or 4K")
    variations: Optional[int] = Field(1, description="Number of variations (1-10)")


class ThumbnailResponse(BaseModel):
    """Response model for generated thumbnails"""
    id: str
    image_urls: List[str]
    prompt: str
    status: str
    created_at: str


class FaceConsistencyRequest(BaseModel):
    """Request for face consistency processing"""
    source_image_url: str = Field(..., description="Base thumbnail image")
    face_reference_url: str = Field(..., description="Reference face image")


# ============== Health Check ==============

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "1.0.0"}


# ============== Thumbnail Generation ==============

@app.post("/api/generate", response_model=ThumbnailResponse)
async def generate_thumbnail(request: ThumbnailRequest):
    """
    Generate AI thumbnail using FLUX.1 model
    """
    try:
        # Build prompt based on style
        style_prompts = {
            "youtube": "YouTube thumbnail, bold colors, high contrast, expressive, clickbait style, 16:9 aspect ratio",
            "minimal": "Clean minimal thumbnail, professional, simple text, muted colors, 16:9 aspect ratio",
            "gaming": "Gaming thumbnail, neon colors, dynamic, action shot, dramatic lighting, 16:9 aspect ratio",
            "tutorial": "Educational thumbnail, clear text, professional, step-by-step style, 16:9 aspect ratio",
            "vlog": "Vlog thumbnail, personal, authentic, warm colors, lifestyle aesthetic, 16:9 aspect ratio"
        }

        base_prompt = f"{request.prompt}, {style_prompts.get(request.style, style_prompts['youtube'])}"

        if request.text_overlay:
            base_prompt += f", text overlay: '{request.text_overlay}'"

        # Resolution settings
        resolution_map = {
            "720p": (1280, 720),
            "1080p": (1920, 1080),
            "4K": (3840, 2160)
        }
        width, height = resolution_map.get(request.resolution, (1920, 1080))

        # Generate with FLUX.1 Schnell (fast, cost-effective)
        output = replicate.run(
            "black-forest-labs/flux-schnell",
            input={
                "prompt": base_prompt,
                "aspect_ratio": "16:9",
                "output_format": "webp",
                "output_quality": 90,
                "num_inference_steps": 4  # Fast generation
            }
        )

        # Handle output (Replicate returns a list of image URLs)
        image_urls = output if isinstance(output, list) else [output]

        return ThumbnailResponse(
            id=f"thumb_{os.urandom(8).hex()}",
            image_urls=image_urls,
            prompt=request.prompt,
            status="completed",
            created_at="now"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


@app.post("/api/generate/pro", response_model=ThumbnailResponse)
async def generate_thumbnail_pro(request: ThumbnailRequest):
    """
    Generate high-quality thumbnail using FLUX.1 Pro
    Better quality, higher cost
    """
    try:
        style_prompts = {
            "youtube": "YouTube thumbnail, professional quality, bold colors, high contrast, expressive, 16:9",
            "minimal": "Minimalist design, clean typography, professional, 16:9 aspect ratio",
            "gaming": "Gaming thumbnail, esports quality, neon accents, dynamic composition, 16:9",
            "tutorial": "Educational content, clear hierarchy, professional design, 16:9",
            "vlog": "Lifestyle vlog, authentic aesthetic, warm tones, personal branding, 16:9"
        }

        base_prompt = f"{request.prompt}, {style_prompts.get(request.style, style_prompts['youtube'])}"

        # Generate with FLUX.1 Pro (higher quality)
        output = replicate.run(
            "black-forest-labs/flux-pro",
            input={
                "prompt": base_prompt,
                "aspect_ratio": "16:9",
                "output_format": "webp",
                "output_quality": 95,
                "num_inference_steps": 28  # Higher quality
            }
        )

        image_urls = output if isinstance(output, list) else [output]

        return ThumbnailResponse(
            id=f"thumb_pro_{os.urandom(8).hex()}",
            image_urls=image_urls,
            prompt=request.prompt,
            status="completed",
            created_at="now"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pro generation failed: {str(e)}")


# ============== Face Consistency ==============

@app.post("/api/face-swap")
async def face_swap(request: FaceConsistencyRequest):
    """
    Apply face consistency using InsightFace
    Preserves creator's face across all thumbnails
    """
    try:
        # Use InsightFace via Replicate
        output = replicate.run(
            "lucataco/insightface:2a2818a0d70e7e6a5d6b5c0e0e0e0e0e",
            input={
                "source_image": request.source_image_url,
                "target_image": request.face_reference_url
            }
        )

        return {
            "id": f"face_{os.urandom(8).hex()}",
            "result_url": output,
            "status": "completed"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Face swap failed: {str(e)}")


# ============== Batch Generation ==============

@app.post("/api/generate/batch")
async def generate_batch(request: ThumbnailRequest):
    """
    Generate multiple variations for A/B testing
    """
    try:
        variations = min(request.variations, 10)  # Max 10
        image_urls = []

        for i in range(variations):
            # Add variation seed to prompt
            varied_prompt = f"{request.prompt}, variation {i+1}, unique composition"

            output = replicate.run(
                "black-forest-labs/flux-schnell",
                input={
                    "prompt": varied_prompt,
                    "aspect_ratio": "16:9",
                    "output_format": "webp",
                    "seed": i * 42  # Different seed for each variation
                }
            )

            if isinstance(output, list):
                image_urls.extend(output)
            else:
                image_urls.append(output)

        return ThumbnailResponse(
            id=f"batch_{os.urandom(8).hex()}",
            image_urls=image_urls,
            prompt=request.prompt,
            status="completed",
            created_at="now"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch generation failed: {str(e)}")


# ============== Templates ==============

TEMPLATES = [
    {"id": "bold_text", "name": "Bold Text", "description": "Large text, high contrast"},
    {"id": "face_closeup", "name": "Face Closeup", "description": "Expressive face, emotional"},
    {"id": "before_after", "name": "Before/After", "description": "Split comparison"},
    {"id": "listicle", "name": "Listicle", "description": "Numbered list style"},
    {"id": "question", "name": "Question", "description": "Curiosity-provoking question"},
    {"id": "reaction", "name": "Reaction", "description": "Shocked/surprised expression"},
    {"id": "tutorial", "name": "Tutorial", "description": "Step-by-step preview"},
    {"id": "gaming", "name": "Gaming", "description": "Action shot, neon colors"},
]

@app.get("/api/templates")
async def get_templates():
    """Get available thumbnail templates"""
    return {"templates": TEMPLATES}


# ============== Usage Tracking ==============

class UsageResponse(BaseModel):
    thumbnails_generated: int
    thumbnails_remaining: int
    subscription_tier: str

@app.get("/api/usage")
async def get_usage(authorization: Optional[str] = Header(None)):
    """Get user's usage statistics"""
    # TODO: Implement database lookup
    return UsageResponse(
        thumbnails_generated=0,
        thumbnails_remaining=50,
        subscription_tier="starter"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
