class Config:
    def __init__(self):
        self.DEFAULT_IGNORED_DIRECTORIES = frozenset({
            ".git",
            ".idea",
            ".vscode",
            ".venv",
            "venv",
            "__pycache__",
            ".pytest_cache",
            ".mypy_cache",
            ".ruff_cache",
            "node_modules",
            "dist",
            "build",
            "coverage",
        })

        self.DEFAULT_IGNORED_FILES = frozenset({
            ".DS_Store",
            "Thumbs.db",
        })

        self.DEFAULT_IGNORED_SUFFIXES = frozenset({
            ".pyc",
            ".pyo",
            ".class",
            ".exe",
            ".dll",
            ".so",
            ".zip",
            ".tar",
            ".gz",
            ".7z",
            ".png",
            ".jpg",
            ".jpeg",
            ".gif",
            ".ico",
            ".mp3",
            ".mp4",
            ".mov",
            ".pdf",
            ".doc",
            ".docx",
        })
    