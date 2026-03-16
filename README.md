# ShopOur-banned-detection
## 🚫 Banned Product Detection Pipeline

An AI-powered product moderation system designed to detect illegal or restricted products in e-commerce listings using text analysis, OCR, and computer vision. This project provides an automated moderation pipeline to detect these listings.

---

## The system analyzes:
- Product title
- Product description
- Image content
- Text inside images (OCR)
- and determines whether a product should be allowed or banned.

---

## Built with:
- FastAPI
- YOLO-World (object detection)
- Tesseract OCR
- RapidFuzz keyword matching

---

## 🧠 E-commerce platforms often struggle with detecting listings containing:
- Illegal drugs
- Weapons
- Fake documents
- Wildlife trafficking products
- Adult products
- Cybercrime tools
- Gambling services
- Tobacco/alcohol/vape products


 

---

## Workflow:

```
Product Input
    │
    │
    ▼
Text Extraction
(title + description)
    │
    │
    ▼
Image Processing
   ├── YOLO Object Detection
   └── OCR Text Extraction
    │
    │
    ▼
Merged Product Text
(title + description + detected objects + OCR)
    │
    │
    ▼
Keyword & Fuzzy Matching
(RapidFuzz)
    │
    │
    ▼
Decision Engine
    │
    ▼
Allowed / Banned

```


