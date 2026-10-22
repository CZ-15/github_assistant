from services.repo_analyzer import RepoAnalyzer
import pytest
from agent import GithubAssistant
from pathlib import Path


@pytest.fixture
def repo_analyzer() -> RepoAnalyzer:
    assistant = GithubAssistant()
    return RepoAnalyzer(assistant)


def test_file_load_reads_content(
    repo_analyzer: RepoAnalyzer,
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "example.py"
    content = "hello"
    file_path.write_text(content, encoding = "utf-8")

    result = repo_analyzer.file_load(str(file_path))

    assert len(result) == 1
    assert result[0].line_count == 1
    assert result[0].content == content


def test_file_load_return_file_path(
    repo_analyzer: RepoAnalyzer,
    tmp_path: Path
) -> None:
    file_path = tmp_path / "example.py"
    file_path.write_text("hello", encoding = "utf-8")

    result = repo_analyzer.file_load(str(file_path))

    assert result[0].path == str(file_path)


def test_file_load_raises_file_not_found(
    repo_analyzer: RepoAnalyzer,
    tmp_path: Path
) -> None:
    non_existent_file = tmp_path / "non_existent.py"

    with pytest.raises(FileNotFoundError):
        repo_analyzer.file_load(str(non_existent_file))


def test_file_load_raises_is_a_directory(
    repo_analyzer: RepoAnalyzer,
    tmp_path: Path
) -> None:
    directory_path = tmp_path / "example_dir"
    directory_path.mkdir()

    with pytest.raises(IsADirectoryError):
        repo_analyzer.file_load(str(directory_path))


def test_file_load_counts_last_line_without_newline(
    repo_analyzer: RepoAnalyzer,
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "README.md"
    file_path.write_text(
        "first line\nsecond line",
        encoding="utf-8",
    )

    result = repo_analyzer.file_load(str(file_path))

    assert result[0].line_count == 2  
    
    

