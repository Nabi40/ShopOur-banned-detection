# banned_detector/utils/vision/object_prompts.py

CATEGORY_PROMPTS = {
    "drugs": [
        "drug packet",
        "cannabis product",
        "marijuana package",
        "medicine bottle",
        "pill blister pack",
        "syrup bottle",
        "powder drug packet",
    ],
    "weapons": [
        "gun",
        "pistol",
        "rifle",
        "ammunition",
        "knife",
        "explosive",
        "fireworks",
    ],
    "human_samples": [
        "blood bag",
        "medical specimen",
        "pathology sample",
    ],
    "wildlife": [
        "ivory carving",
        "animal horn",
        "wildlife trophy",
        "protected animal product",
    ],
    "fraud_docs": [
        "passport",
        "identity card",
        "bank card",
        "sim card",
        "driving license",
        "birth certificate",
    ],
    "cybercrime": [
        "hacking tool box",
        "phishing kit screen",
        "password cracking software interface",
    ],
    "gambling": [
        "casino chips",
        "betting slip",
        "slot machine",
        "lottery ticket",
    ],
    "adult": [
        "pornographic material",
        "explicit adult content",
    ],
    "alcohol_tobacco_vape": 
    [
        "cigarette",
        "cigarette pack",
        "person smoking",
        "smoking cigarette",
        "vape device",
        "e cigarette",
        "alcohol bottle",
        "beer bottle",
        "wine bottle",
        "liquor bottle",
        ]
}