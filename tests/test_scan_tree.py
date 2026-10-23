from pathlib import Path

import pytest

from agent import GithubAssistant
from services.repo_analyzer import RepoAnalyzer


@pytest.fixture
def repo_analyzer() -> RepoAnalyzer:
    assistant = GithubAssistant()
    return RepoAnalyzer(assistant)


def test_scan_tree_returns_empty_list_for_empty_directory(
    repo_analyzer: RepoAnalyzer,
    tmp_path: Path,
):
    result = repo_analyzer.scan_tree(str(tmp_path))

    assert result == []


def test_scan_tree_returns_file_information(
    repo_analyzer: RepoAnalyzer,
    tmp_path: Path,
):
    source_directory = tmp_path / "src"
    source_directory.mkdir()

    file_path = source_directory / "main.py"
    content = "print('hello')\n"
    file_path.write_text(content, encoding="utf-8")

    result = repo_analyzer.scan_tree(str(tmp_path))

    assert len(result) == 1
    scanned_file = result[0]
    assert scanned_file.relative_path == "src/main.py"
    assert scanned_file.suffix == ".py"
    assert scanned_file.size == file_path.stat().st_size


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
def test_scan_tree_ignores_directories(
    repo_analyzer: RepoAnalyzer,
    tmp_path: Path,
    dir_name: str,
):
    ignored_directory = tmp_path / dir_name
    ignored_directory.mkdir()
    ignored_file = ignored_directory / "ignored.py"
    ignored_file.write_text("print('ignored')", encoding="utf-8")

    included_file = tmp_path / "included.py"
    included_file.write_text("print('included')", encoding="utf-8")

    result = repo_analyzer.scan_tree(str(tmp_path))
    relative_paths = [file.relative_path for file in result]

    assert relative_paths == ["included.py"]
    assert f"{dir_name}/ignored.py" not in relative_paths


@pytest.mark.parametrize("file_name", [".DS_Store", "Thumbs.db"])
def test_scan_tree_ignores_files_by_name(
    repo_analyzer: RepoAnalyzer,
    tmp_path: Path,
    file_name: str,
):
    ignored_file = tmp_path / file_name
    ignored_file.write_bytes(b"ignored")

    included_file = tmp_path / "README.md"
    included_file.write_text("# Project", encoding="utf-8")

    result = repo_analyzer.scan_tree(str(tmp_path))
    relative_paths = [file.relative_path for file in result]

    assert relative_paths == ["README.md"]
    assert file_name not in relative_paths


@pytest.mark.parametrize(
    "suffix",
    [
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
    ],
)
def test_scan_tree_ignores_files_by_suffix(
    repo_analyzer: RepoAnalyzer,
    tmp_path: Path,
    suffix: str,
):
    ignored_file = tmp_path / f"ignored{suffix}"
    ignored_file.write_bytes(b"ignored")

    included_file = tmp_path / "included.py"
    included_file.write_text("print('included')", encoding="utf-8")

    result = repo_analyzer.scan_tree(str(tmp_path))
    relative_paths = [file.relative_path for file in result]

    assert relative_paths == ["included.py"]
    assert ignored_file.name not in relative_paths


def test_scan_tree_ignores_uppercase_suffix(
    repo_analyzer: RepoAnalyzer,
    tmp_path: Path,
):
    ignored_file = tmp_path / "image.PNG"
    ignored_file.write_bytes(b"image")

    result = repo_analyzer.scan_tree(str(tmp_path))

    assert result == []


def test_scan_tree_uses_forward_slashes_in_relative_path(
    repo_analyzer: RepoAnalyzer,
    tmp_path: Path,
):
    nested_directory = tmp_path / "src" / "utils"
    nested_directory.mkdir(parents=True)

    file_path = nested_directory / "helper.py"
    file_path.write_text("def helper(): pass", encoding="utf-8")

    result = repo_analyzer.scan_tree(str(tmp_path))

    assert len(result) == 1
    assert result[0].relative_path == "src/utils/helper.py"


def test_scan_tree_root_is_dir(
    repo_analyzer,
    tmp_path,
):
    file_path = tmp_path / "main.py"
    file_path.write_text("print('hello')", encoding="utf-8")

    with pytest.raises(
        NotADirectoryError,
        match="is not a directory",
    ):
        repo_analyzer.scan_tree(str(file_path))


def test_scan_tree_root_does_not_exist(
    repo_analyzer,
    tmp_path,
):
    non_existent_path = tmp_path / "non_existent_dir"

    with pytest.raises(
        FileNotFoundError,
        match="does not exist",
    ):
        repo_analyzer.scan_tree(str(non_existent_path))