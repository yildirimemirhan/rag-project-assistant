"""Project routing: map a query to a known project key. Pure Python, no heavy imports."""

KNOWN_PROJECTS = [
    "wbc-analyzer",
    "kinematic",
    "listing-pilot",
    "popcorn-wagon",
    "portal-cleaner-ultimate",
    "crm-aspnetcore",
    "rag-project-assistant",
    "research",
    "profile",
]

# Order matters: first match wins. Specific projects come before "profile".
PROJECT_KEYWORDS = {
    "wbc-analyzer": ["wbc", "wbc analyzer", "wbc-analyzer", "white blood cell", "arayüz", "hücre", "densenet", "mef", "grad-cam", "gradcam", "medsiwsh", "wbcattention"],
    "listing-pilot": ["listing pilot", "listing-pilot", "dolap", "gardrops", "appium", "fiyat", "listing"],
    "kinematic": ["kinematic", "hareket", "action recognition", "dask", "arf", "adwin", "motion"],
    "popcorn-wagon": ["popcorn wagon", "popcorn-wagon", "film", "movie", "öneri", "recommendation", "svd", "annoy"],
    "portal-cleaner-ultimate": ["portal cleaner", "portal-cleaner", "portal", "erp", "tkinter", "selenium scraper"],
    "crm-aspnetcore": ["crm", "asp.net", "aspnet", "entity framework", "razor", "esbi"],
    "rag-project-assistant": ["rag project assistant", "rag-project-assistant", "retrieval-augmented", "rag system", "rag pipeline", "this assistant", "this chatbot", "chromadb", "similarity threshold", "similarity-threshold"],
    "research": ["thesis", "research project", "microscopy", "stain", "segmentation", "video processing", "temporal consistency", "tez", "araştırma"],
    "profile": [
        "resume", "cv ", "education", "university", "degree", "m.sc", "msc", "master's", "bachelor",
        "certif", "contact", "email", "linkedin", "experience", "internship", "zidorun", "platech",
        "available", "availability", "hire", "hiring", "open to", "language", "yokdil", "publication",
        "preprint", "who is", "about emirhan", "background", "skills", "tech stack", "location",
        "özgeçmiş", "eğitim", "iletişim", "deneyim", "yetenek",
    ],
}


def detect_project(query: str) -> str | None:
    q = query.lower()
    for project, keywords in PROJECT_KEYWORDS.items():
        if any(kw in q for kw in keywords):
            return project
    return None


def extract_project(filename: str) -> str:
    """Map a documents/ filename to its project key. Longest prefix wins."""
    for p in sorted(KNOWN_PROJECTS, key=len, reverse=True):
        if filename.startswith(p):
            return p
    return "unknown"
