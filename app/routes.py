import os
import httpx
from fastapi import APIRouter, UploadFile, File
from dotenv import load_dotenv
from .utils import encode_image_to_base64
from .utils import clean_markdown_json
import json

load_dotenv()
router = APIRouter()

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
API_KEY = os.getenv("GEMINI_API_KEY")

@router.post("/identify-plant")
async def identify_plant(image: UploadFile = File(...)):
    content = await image.read()
    img_base64 = encode_image_to_base64(content)

    payload = {
        "contents": [{
            "parts": [
                {
                    "inlineData": {
                        "mimeType": image.content_type,
                        "data": img_base64
                    }
                },
                {
                "text": "Tolong identifikasi tanaman ini dan berikan penjelasan menarik untuk anak-anak. \
                        Gunakan format JSON dengan struktur berikut:\n\n{\n  \"plant_name\": string,\n  \"description\": string,\n  \"care_tips\": [string]\n}\n\nJawab hanya dengan format JSON."
                }
            ]
        }]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{GEMINI_URL}?key={API_KEY}",
            json=payload,
            timeout=30.0
        )
    gemini_data = response.json()
    raw_text = gemini_data['candidates'][0]['content']['parts'][0]['text']
    raw_text = clean_markdown_json(raw_text)
    try:
        structured_data = json.loads(raw_text)
    except json.JSONDecodeError:
        structured_data = {"raw_text": raw_text}

    return structured_data
