from pathlib import Path
import shutil
import tempfile

from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from utils.pipeline import BannedProductPipeline

app = FastAPI(title="Banned Product Detection API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = BannedProductPipeline()


@app.get("/")
def root():
    return {
        "message": "Banned Product Detection API is running"
    }


@app.post("/check-product")
async def check_product(
    title: str = Form(default=""),
    description: str = Form(default=""),
    image: UploadFile | None = File(default=None),
):
    if not title.strip() and not description.strip() and image is None:
        raise HTTPException(
            status_code=400,
            detail="Provide at least one of: title, description, or image."
        )

    temp_path = None

    try:
        if image is not None:
            suffix = Path(image.filename).suffix if image.filename else ".jpg"
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                shutil.copyfileobj(image.file, tmp)
                temp_path = tmp.name

        result = pipeline.run(
            title=title,
            description=description,
            image_path=temp_path,
        )
        return result

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    finally:
        if image is not None:
            image.file.close()
        if temp_path and Path(temp_path).exists():
            Path(temp_path).unlink(missing_ok=True)