# banned_detector/utils/vision/yolo_world_detector.py

from typing import Dict, Any, List

try:
    from ultralytics import YOLO
except Exception:
    YOLO = None

try:
    import torch
    from PIL import Image
    from transformers import CLIPProcessor, CLIPModel
except Exception:
    torch = None
    Image = None
    CLIPProcessor = None
    CLIPModel = None


FALLBACK_LABELS = [
    "cigarette",
    "smoking",
    "vape",
    "gun",
    "knife",
    "alcohol bottle",
    "medicine bottle",
    "syringe",
    "passport",
    "credit card",
    "orange",
    "apple",
    "bicycle",
    "lipstick",
    "shoe",
    "phone",
    "bag",
]


class YoloWorldDetector:
    def __init__(self, model_name: str = "yolov8n.pt"):
        self.model = None
        self.model_name = model_name

        if YOLO is not None:
            try:
                self.model = YOLO(model_name)
            except Exception:
                self.model = None

        self.clip_model = None
        self.clip_processor = None
        self.device = "cuda" if torch and torch.cuda.is_available() else "cpu"

        if CLIPModel is not None and CLIPProcessor is not None:
            try:
                self.clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(self.device)
                self.clip_model.eval()
                self.clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
            except Exception:
                self.clip_model = None
                self.clip_processor = None

    def is_ready(self) -> bool:
        return self.model is not None

    def _clip_fallback_labels(self, image_path: str) -> List[str]:
        if self.clip_model is None or self.clip_processor is None or Image is None:
            return []

        try:
            image = Image.open(image_path).convert("RGB")
            inputs = self.clip_processor(
                text=FALLBACK_LABELS,
                images=image,
                return_tensors="pt",
                padding=True,
                truncation=True,
            ).to(self.device)

            with torch.no_grad():
                outputs = self.clip_model(**inputs)
                logits = outputs.logits_per_image[0]
                probs = logits.softmax(dim=0).detach().cpu().tolist()

            ranked = sorted(zip(FALLBACK_LABELS, probs), key=lambda x: x[1], reverse=True)
            return [label for label, score in ranked[:2] if score >= 0.08]

        except Exception:
            return []

    def detect(self, image_path: str) -> Dict[str, Any]:
        if not self.is_ready():
            return {
                "success": False,
                "labels": [],
                "score": 0.0,
                "detections": [],
                "error": "YOLO model not available.",
            }

        try:
            results = self.model.predict(
                source=image_path,
                conf=0.35,
                verbose=False,
            )

            labels: List[str] = []
            detections: List[Dict[str, Any]] = []
            best_score = 0.0

            for r in results:
                names = r.names
                if r.boxes is None:
                    continue

                for box in r.boxes:
                    cls_id = int(box.cls[0].item())
                    conf = float(box.conf[0].item())
                    label = names.get(cls_id, str(cls_id))

                    labels.append(label)
                    detections.append({
                        "label": label,
                        "score": round(conf, 4),
                    })

                    if conf > best_score:
                        best_score = conf

            labels = sorted(set(labels))

            # fallback if labels are empty or too generic
            generic_labels = {"person", "toothbrush", "cell phone", "bottle"}
            if not labels or set(labels).issubset(generic_labels):
                fallback = self._clip_fallback_labels(image_path)
                for f in fallback:
                    if f not in labels:
                        labels.append(f)
                        detections.append({
                            "label": f,
                            "score": 0.1,
                        })

            labels = sorted(set(labels))

            return {
                "success": True,
                "labels": labels,
                "score": round(best_score, 4),
                "detections": detections,
                "error": None,
            }

        except Exception as exc:
            return {
                "success": False,
                "labels": [],
                "score": 0.0,
                "detections": [],
                "error": str(exc),
            }