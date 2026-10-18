from models import schemas
import json
from pathlib import Path


class RepoAnalyzer:
    def scan_tree(self, repository_path: str) -> 

    def load(self, repository_path: str) -> list[schemas.RepositoryFile]:  ## 仓库的读取
        repository_files = []  

        repositoryfile = schemas.RepositoryFile(path=repository_path, content="", line_count=0)
        """json文件传化为python"""
        with open(repositoryfile.path, "r", encoding = "UTF-8") as f:
            if repositoryfile.path.is_file() and repositoryfile.path.suffix.lower() == ".json":
                repositoryfile.content = json.load(f)
                repositoryfile.line_count = len(repositoryfile.path.read_text(encoding="utf-8").splitlines())
            else:  ## python文件读取
                for line in f:
                    repositoryfile.content += line
                    repositoryfile.line_count += 1
        repository_files.append(repositoryfile)
        return repository_files  ## 暂时不确定

"""
    def file_filter(self, repository_files: list[schemas.RepositoryFile]) -> dict:  ## 仓库的分析
"""
