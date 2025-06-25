import base64

def encode_image_to_base64(file_bytes: bytes) -> str:
    return base64.b64encode(file_bytes).decode("utf-8")

def clean_markdown_json(raw_text: str) -> str:
    lines = raw_text.strip().splitlines()
    if lines[0].strip().startswith("```") and lines[-1].strip().endswith("```"):
        return "\n".join(lines[1:-1]).strip()
    return raw_text.strip()