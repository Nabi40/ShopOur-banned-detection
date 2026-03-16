# banned_detector/utils/schemas/response_schema.py

from typing import Any, Dict


def build_response(
    title: str,
    description: str,
    detector_result: Dict[str, Any],
    ocr_result: Dict[str, Any],
    merged_text: str,
    merged_text_result: Dict[str, Any],
    decision_result: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "input": {
            "title": title,
            "description": description,
            "image_used": bool(detector_result or ocr_result),
        },
        "decision": decision_result,
        "product_detection": {
            "detected_labels": detector_result.get("labels", []),
            "detector_score": detector_result.get("score", 0.0),
            "detections": detector_result.get("detections", []),
        },
        "ocr": ocr_result,
        "merged_text": merged_text,
        "merged_text_analysis": merged_text_result,
    }