# banned_detector/utils/pipeline.py

from typing import Any, Dict, Optional

from utils.text.text_detector import analyze_text
from utils.ocr.image_ocr import extract_text_from_image
from utils.vision.yolo_world_detector import YoloWorldDetector
from utils.decision.decision_engine import decide
from utils.schemas.response_schema import build_response


class BannedProductPipeline:
    def __init__(self) -> None:
        self.yolo_detector = None

    def _get_yolo_detector(self):
        if self.yolo_detector is None:
            self.yolo_detector = YoloWorldDetector()
        return self.yolo_detector

    def run(
        self,
        title: str = "",
        description: str = "",
        image_path: Optional[str] = None,
    ) -> Dict[str, Any]:
        detector_result = {
            "success": False,
            "labels": [],
            "score": 0.0,
            "detections": [],
            "error": "Skipped.",
        }

        ocr_result = {
            "text": "",
            "success": False,
            "error": "Skipped.",
        }

        image_labels_text = ""
        ocr_text = ""

        if image_path:
            detector_result = self._get_yolo_detector().detect(image_path)
            image_labels = detector_result.get("labels", [])
            image_labels_text = " ".join(image_labels)

            ocr_result = extract_text_from_image(image_path)
            ocr_text = ocr_result.get("text", "") or ""

        merged_text = " ".join(
            part.strip()
            for part in [title, description, image_labels_text, ocr_text]
            if part and part.strip()
        ).strip()

        merged_text_result = analyze_text(
            title=merged_text,
            description="",
        )

        decision_result = decide(
            merged_text_result=merged_text_result,
        )

        return build_response(
            title=title,
            description=description,
            detector_result=detector_result,
            ocr_result=ocr_result,
            merged_text=merged_text,
            merged_text_result=merged_text_result,
            decision_result=decision_result,
        )