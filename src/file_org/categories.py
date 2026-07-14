CATEGORIES: dict[str, tuple[str, ...]] = {
    "Images": (
        ".jpg", ".jpeg", ".png", ".gif", ".webp",
        ".svg", ".bmp", ".ico", ".tiff", ".avif",
    ),
    "Video": (
        ".mp4", ".webm", ".mov", ".avi", ".mkv",
        ".flv", ".wmv", ".m4v",
    ),
    "Audio": (
        ".mp3", ".wav", ".flac", ".aac", ".ogg",
        ".wma", ".m4a", ".opus",
    ),
    "Documents": (
        ".pdf", ".doc", ".docx", ".xls", ".xlsx",
        ".ppt", ".pptx", ".odt", ".ods", ".odp",
        ".txt", ".rtf", ".md", ".tex",
    ),
    "Archives": (
        ".zip", ".tar", ".gz", ".rar", ".7z",
        ".bz2", ".xz", ".zst",
    ),
    "Code": (
        ".py", ".js", ".ts", ".jsx", ".tsx",
        ".cpp", ".c", ".h", ".hpp", ".rs",
        ".go", ".java", ".rb", ".php", ".swift",
        ".kt", ".scala", ".lua",
    ),
    "Data": (
        ".csv", ".json", ".xml", ".yaml", ".yml",
        ".toml", ".ini", ".cfg",
    ),
    "Installers": (
        ".iso", ".dmg", ".exe", ".msi", ".deb",
        ".rpm", ".pkg", ".AppImage",
    ),
}

UNCATEGORISED = "Misc"
