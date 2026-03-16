# banned_detector/utils/vision/grounding_dino_detector.py

from typing import Any, Dict, List

from utils.vision.object_prompts import CATEGORY_PROMPTS

try:
    from transformers import pipeline
except Exception:
    pipeline = None


class GroundingDinoDetector:
    def __init__(self, model_name: str = "IDEA-Research/grounding-dino-base"):
        self.model_name = model_name
        self.detector = None

        if pipeline is not None:
            try:
                self.detector = pipeline(
                    task="zero-shot-object-detection",
                    model=model_name,
                )
            except Exception:
                self.detector = None

    def is_ready(self) -> bool:
        return self.detector is not None

    def detect(self, image_path: str) -> Dict[str, Any]:
        if not self.detector:
            return {
                "success": False,
                "score": 0.0,
                "detections": [],
                "categories": [],
                "error": "Grounding DINO model is not available.",
            }

        all_detections: List[Dict[str, Any]] = []
        matched_categories = set()
        max_score = 0.0

        try:
            for category, prompts in CATEGORY_PROMPTS.items():
                outputs = self.detector(image_path, candidate_labels=prompts)

                for item in outputs:
                    score = float(item.get("score", 0.0))
                    label = item.get("label", "")
                    box = item.get("box", {})

                    if score >= 0.50:
                        all_detections.append({
                            "category": category,
                            "label": label,
                            "score": round(score, 4),
                            "box": box,
                        })
                        matched_categories.add(category)
                        max_score = max(max_score, score)

            return {
                "success": True,
                "score": round(max_score, 4),
                "detections": all_detections,
                "categories": sorted(matched_categories),
                "error": None,
            }
        except Exception as exc:
            return {
                "success": False,
                "score": 0.0,
                "detections": [],
                "categories": [],
                "error": str(exc),
            }