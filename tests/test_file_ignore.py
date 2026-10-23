from services.repo_analyzer import RepoAnalyzer
import pytest   
from agent import GithubAssistant
from pathlib import Path


@pytest.fixture
def repo_analyzer() -> RepoAnalyzer:
    assistant = GithubAssistant()
    return RepoAnalyzer(assistant)


@pytest.mark.parametrize(
    "dir_name",
    [
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
    ],
)
def test_file_ignore_default_ignored_directories(
    repo_analyzer: RepoAnalyzer,
    tmp_path: Path,
    dir_name: str
) -> None:
    dir_path = tmp_path / dir_name
    dir_path.mkdir()

    assert  repo_analyzer.file_ignore(dir_path) is True


@pytest.mark.parametrize(
    "file_name",
    [
        ".DS_Store",
        "Thumbs.db",
    ],
)
def test_file_ignore_default_ignored_files(
    repo_analyzer: RepoAnalyzer,
    tmp_path: Path,
    file_name: str
) -> None:
    file_path = tmp_path / file_name
    file_path.write_text("content", encoding = "utf-8")

    assert repo_analyzer.file_ignore(file_path) is True


@pytest.mark.parametrize(
    "file_name",
    [
        "cache.pyc",
        "cache.pyo",
        "Main.class",
        "program.exe",
        "library.dll",
        "library.so",
        "archive.zip",
        "archive.tar",
        "archive.gz",
        "archive.7z",
        "picture.png",
        "picture.jpg",
        "picture.jpeg",
        "picture.gif",
        "favicon.ico",
        "audio.mp3",
        "video.mp4",
        "video.mov",
        "document.pdf",
        "document.doc",
        "document.docx",
    ],
)
def test_file_ignore_default_ignored_suffixes(
    repo_analyzer: RepoAnalyzer,
    tmp_path: Path,
    file_name: str,
) -> None:
    file_path = tmp_path / file_name
    file_path.write_bytes(b"content")

    assert repo_analyzer.file_ignore(file_path) is True


@pytest.mark.parametrize(
    "file_name",
    [
        "cache.pyc",
        "cache.pyo",
        "Main.class",
        "program.exe",
        "library.dll",
        "library.so",
        "archive.zip",
        "archive.tar",
        "archive.gz",
        "archive.7z",
        "picture.png",
        "picture.jpg",
        "picture.jpeg",
        "picture.gif",
        "favicon.ico",
        "audio.mp3",
        "video.mp4",
        "video.mov",
        "document.pdf",
        "document.doc",
        "document.docx",
        "document.DOC",
        "picture.PNG",
        "archive.ZIP",
    ],
)
def test_file_ignore_default_ignored_suffixes(
    repo_analyzer: RepoAnalyzer,
    tmp_path: Path,
    file_name: str,
) -> None:
    file_path = tmp_path / file_name
    file_path.write_text("content", encoding = "utf-8")

    assert repo_analyzer.file_ignore(file_path) is True


@pytest.mark.parametrize(  ## 反向测试正常文件
    "file_name",
    [
        "main.py",
        "README.md",
        "config.json",
        "pyproject.toml",
        "package-lock.json",
    ],
)
def test_file_ignore_keeps_useful_files(
    repo_analyzer: RepoAnalyzer,
    tmp_path: Path,
    file_name: str,
) -> None:
    file_path = tmp_path / file_name
    file_path.write_text(
        "content",
        encoding="utf-8",
    )

    assert repo_analyzer.file_ignore(file_path) is False

