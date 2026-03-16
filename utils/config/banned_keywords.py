# banned_detector/utils/config/banned_keywords.py

from .banned_categories import BANNED_CATEGORIES

CATEGORY_KEYWORDS = BANNED_CATEGORIES

KEYWORD_ALIASES = {

    # ---------------- DRUGS ----------------
    "ganja": [
        "weed", "marijuana", "cannabis", "ganga", "gaja", "pot",
        "hash", "hashish", "charas", "mary jane", "thc", "thc oil",
        "weed vape", "weed oil"
    ],

    "marijuana": [
        "ganja", "weed", "cannabis", "pot", "mary jane",
        "hashish", "hash", "thc"
    ],

    "cannabis": [
        "weed", "ganja", "marijuana", "hash", "thc",
        "cannabis oil", "cannabis resin"
    ],

    "heroin": [
        "smack", "brown sugar", "diamorphine", "horse"
    ],

    "cocaine": [
        "coke", "snow", "blow", "crack cocaine"
    ],

    "methamphetamine": [
        "meth", "crystal meth", "ice", "speed"
    ],

    "mdma": [
        "ecstasy", "molly", "party drug", "e pills"
    ],

    "ecstasy": [
        "mdma", "molly", "club drug"
    ],

    "lsd": [
        "acid", "blotter acid", "lsd blotter"
    ],

    "psilocybin mushrooms": [
        "magic mushrooms", "shrooms"
    ],

    "phensedyl": [
        "cough syrup", "codeine syrup", "phensidyl"
    ],

    "yaba": [
        "meth tablet", "crazy drug"
    ],

    "nitrous oxide": [
        "laughing gas", "n2o", "whippets", "cream charger"
    ],

    # ---------------- WEAPONS ----------------
    "guns": [
        "gun", "firearm", "weapon", "pistol", "rifle",
        "revolver", "shotgun", "handgun", "assault rifle"
    ],

    "pistol": [
        "handgun", "revolver"
    ],

    "rifle": [
        "sniper rifle", "assault rifle", "carbine"
    ],

    "ammunition": [
        "ammo", "bullets", "rounds", "cartridges"
    ],

    "explosives": [
        "bomb", "grenade", "dynamite", "ied",
        "explosive material"
    ],

    "switchblades": [
        "automatic knife", "spring knife"
    ],

    "knife": [
        "combat knife", "dagger", "stiletto", "machete"
    ],

    # ---------------- HUMAN SAMPLES ----------------
    "human organs": [
        "kidney for sale", "liver for sale", "organ transplant organ"
    ],

    "blood": [
        "blood bag", "blood sample", "plasma"
    ],

    "dna samples": [
        "genetic sample", "dna kit"
    ],

    # ---------------- WILDLIFE ----------------
    "ivory": [
        "elephant ivory", "ivory tusk", "ivory carving"
    ],

    "rhino horn": [
        "rhinoceros horn"
    ],

    "tiger parts": [
        "tiger skin", "tiger bone", "tiger tooth"
    ],

    "pangolin": [
        "pangolin scales"
    ],

    "wildlife trophies": [
        "animal trophy", "hunting trophy"
    ],

    # ---------------- FRAUD DOCUMENTS ----------------
    "passports": [
        "passport for sale", "fake passport"
    ],

    "national id cards": [
        "nid card", "national id", "nid"
    ],

    "driving licenses": [
        "driver license", "fake driving license"
    ],

    "credit cards": [
        "stolen credit card", "clone card"
    ],

    "bank accounts for sale": [
        "verified bank account", "bank account ready"
    ],

    "sim cards registered to other people": [
        "registered sim", "pre registered sim"
    ],

    # ---------------- CYBERCRIME ----------------
    "malware": [
        "virus", "trojan", "spyware", "ransomware",
        "keylogger"
    ],

    "phishing kits": [
        "phishing tool", "phishing software"
    ],

    "password cracking software": [
        "password cracker", "wifi password cracker",
        "bruteforce tool"
    ],

    "ddos tools": [
        "booter", "stresser", "ddos attack tool"
    ],

    "botnets": [
        "botnet malware"
    ],

    "credential stealers": [
        "account stealer", "password stealer"
    ],

    # ---------------- GAMBLING ----------------
    "betting services": [
        "sports betting", "online betting"
    ],

    "online gambling services": [
        "online casino", "casino site"
    ],

    "lottery schemes": [
        "lottery scam", "lottery ticket"
    ],

    "casino access products": [
        "casino account", "betting account"
    ],

    # ---------------- ADULT ----------------
    "pornographic videos": [
        "porn", "xxx video", "adult video", "sex video"
    ],

    "sex toys": [
        "adult toys", "intimate toys"
    ],

    "dildos": [
        "sex toy", "adult toy"
    ],

    "vibrators": [
        "adult vibrator", "intimate massager"
    ],

    "bdsm": [
        "bondage gear", "fetish gear"
    ],

    "adult entertainment": [
        "adult service", "escort service"
    ],

    # ---------------- ALCOHOL / TOBACCO / VAPE ----------------
    "cigarettes": [
        "cigarette", "smoking tobacco", "tobacco cigarette"
    ],

    "tobacco": [
        "smoking tobacco", "rolling tobacco"
    ],

    "vape": [
        "e-cigarette", "vaping", "electronic cigarette",
        "ecigarette", "vape pen", "vape device",
        "vape pod", "vape juice", "eliquid"
    ],

    "beer": [
        "alcohol beer"
    ],

    "whiskey": [
        "whisky", "scotch"
    ],

    "vodka": [
        "vodka liquor"
    ],

    "wine": [
        "red wine", "white wine"
    ],

}