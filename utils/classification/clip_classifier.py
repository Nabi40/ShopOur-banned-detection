# banned_detector/utils/classification/clip_classifier.py

from typing import Dict, Any, List, Tuple
from PIL import Image

try:
    import torch
    from transformers import CLIPProcessor, CLIPModel
except Exception:
    torch = None
    CLIPProcessor = None
    CLIPModel = None


CATEGORY_TEXT_PROMPTS = {
    "drugs": [
        "illegal drugs product",
        "cannabis product",
        "drug packet",
    ],
    "weapons": [
        "gun product",
        "weapon for sale",
        "knife weapon",
    ],
    "human_samples": [
        "blood or pathology specimen",
    ],
    "wildlife": [
        "ivory or horn product",
    ],
    "fraud_docs": [
        "passport or id card for sale",
        "bank card or sim card being sold",
    ],
    "cybercrime": [
        "hacking or phishing software product",
    ],
    "gambling": [
        "gambling or betting product",
    ],
    "adult": [
        "explicit adult product",
        "pornographic content cover",
    ],
    "alcohol_tobacco_vape": [
        "cigarette product image",
        "person smoking a cigarette",
        "vape product image",
        "alcohol bottle product image",
    ],



    
}


class ClipCategoryClassifier:
    def __init__(self, model_name: str = "openai/clip-vit-base-patch32"):
        self.model_name = model_name
        self.device = "cuda" if torch and torch.cuda.is_available() else "cpu"
        self.model = None
        self.processor = None

        self.prompt_rows: List[Tuple[str, str]] = []
        self.all_prompts: List[str] = []
        self.text_features = None

        if CLIPModel is not None and CLIPProcessor is not None:
            try:
                self.model = CLIPModel.from_pretrained(model_name).to(self.device)
                self.model.eval()
                self.processor = CLIPProcessor.from_pretrained(model_name)

                for category, prompts in CATEGORY_TEXT_PROMPTS.items():
                    for prompt in prompts:
                        self.prompt_rows.append((category, prompt))

                self.all_prompts = [prompt for _, prompt in self.prompt_rows]
                self._build_text_features()

            except Exception:
                self.model = None
                self.processor = None
                self.text_features = None

    def is_ready(self) -> bool:
        return (
            self.model is not None
            and self.processor is not None
            and self.text_features is not None
        )

    def _build_text_features(self) -> None:
        if self.model is None or self.processor is None:
            return

        with torch.no_grad():
            text_inputs = self.processor(
                text=self.all_prompts,
                return_tensors="pt",
                padding=True,
                truncation=True,
            ).to(self.device)

            text_features = self.model.get_text_features(
                input_ids=text_inputs["input_ids"],
                attention_mask=text_inputs["attention_mask"],
            )

            text_features = text_features / text_features.norm(dim=-1, keepdim=True)
            self.text_features = text_features

    def _load_image(self, image_path: str) -> Image.Image:
        image = Image.open(image_path).convert("RGB")

        max_side = 512
        w, h = image.size
        longest = max(w, h)

        if longest > max_side:
            scale = max_side / longest
            new_size = (int(w * scale), int(h * scale))
            image = image.resize(new_size)

        return image

    def classify(self, image_path: str) -> Dict[str, Any]:
        if not self.is_ready():
            return {
                "success": False,
                "score": 0.0,
                "best_category": None,
                "best_prompt": None,
                "category_scores": {},
                "error": "CLIP model is not available.",
            }

        try:
            image = self._load_image(image_path)

            with torch.no_grad():
                image_inputs = self.processor(
                    images=image,
                    return_tensors="pt",
                ).to(self.device)

                image_features = self.model.get_image_features(
                    pixel_values=image_inputs["pixel_values"]
                )
                image_features = image_features / image_features.norm(dim=-1, keepdim=True)

                similarities = (image_features @ self.text_features.T)[0]
                probs = similarities.softmax(dim=0).detach().cpu().numpy()

            category_scores: Dict[str, float] = {}
            best_category = None
            best_prompt = None
            best_score = 0.0

            for (category, prompt), score in zip(self.prompt_rows, probs):
                score = float(score)

                if category not in category_scores or score > category_scores[category]:
                    category_scores[category] = score

                if score > best_score:
                    best_score = score
                    best_category = category
                    best_prompt = prompt

            return {
                "success": True,
                "score": round(best_score, 4),
                "best_category": best_category,
                "best_prompt": best_prompt,
                "category_scores": {k: round(v, 4) for k, v in category_scores.items()},
                "error": None,
            }

        except Exception as exc:
            return {
                "success": False,
                "score": 0.0,
                "best_category": None,
                "best_prompt": None,
                "category_scores": {},
                "error": str(exc),
            }