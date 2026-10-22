from services.repo_analyzer import RepoAnalyzer
import pytest
from agent import GithubAssistant
from pathlib import Path


@pytest.fixture
def repo_analyzer() -> RepoAnalyzer:
    assistant = GithubAssistant()
    return RepoAnalyzer(assistant)


def test_file_load(
    repo_analyzer: RepoAnalyzer,
    tmp_path: Path,
) -> None:
    
    
    

