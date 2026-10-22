from models import schemas
import json
from pathlib import Path


class RepoAnalyzer:
    def __init__(self, assistant):  ## assistant是GithubAssistant(在agent.py里)的实例
        self.assistant = assistant  ## 传入assistant实例，方便RepoAnalyzer访问GithubAssistant的属性和方法
        self.cfg = assistant.cfg

    
    def file_ignore(self, path: Path) -> bool:  ## path是具体文件或者文件夹的路径
        if path.is_dir() and path.name in self.cfg.DEFAULT_IGNORED_DIRECTORIES:
            return True

        if path.is_file() and path.name in self.cfg.DEFAULT_IGNORED_FILES:
            return True

        if path.is_file() and path.suffix.lower() in self.cfg.DEFAULT_IGNORED_SUFFIXES:
            return True

        return False


    def scan_tree(self, repository_path: str) -> list[schemas.FileBase]:  ## 仓库的扫描
        pass
        

        
    def file_load(self, repo_path: str) -> list[schemas.RepositoryFile]:  ## 仓库的读取
        repository_files = []  

        repositoryfile = schemas.RepositoryFile(path=repo_path, content="", line_count=0)  ## ## 创建一个RepositoryFile对象，初始化路径、内容和行数
        file_path = Path(repositoryfile.path).resolve()  ## 转为Path对象

        """json文件传化为python"""
        with open(file_path, "r", encoding = "UTF-8") as f:
            if file_path.is_file() and file_path.suffix.lower() == ".json":
                repositoryfile.content = json.load(f)
                repositoryfile.line_count = len(file_path.read_text(encoding="utf-8").splitlines())

            else:  ## python文件读取
                for line in f:
                    repositoryfile.content += line
                    repositoryfile.line_count += 1
        repository_files.append(repositoryfile)
        return repository_files  ## 暂时不确定

"""
    def file_filter(self, repository_files: list[schemas.RepositoryFile]) -> dict:  ## 仓库的分析
"""
