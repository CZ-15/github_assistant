from models import schemas
from pathlib import Path
import os


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
        root = Path(repository_path).resolve()

        if not root.exists():
            raise FileNotFoundError(f"Repository path '{repository_path}' does not exist.")
        if not root.is_dir():
            raise NotADirectoryError(f"Repository path '{repository_path}' is not a directory.")

        files_tree: list[schemas.FileBase] = []

        for current_dir, dir_names, file_name in os.walk(
            root,
            topdown=True,
            followlinks=False,
        ):
            current_path = Path(current_dir)
            dir_names[:] = sorted(
                name
                for name in dir_names
                if not self.file_ignore(current_path / name)
                and not (current_path / name).is_symlink()   
            )

            for file in sorted(file_name):
                file_path = current_path / file
                
                if self.file_ignore(file_path) or file_path.is_symlink():
                    continue

                try:
                    size = file_path.stat().st_size
                except OSError:
                    print(f"Warning: Could not access file '{file_path}'. Skipping.")
                    continue

                files_tree.append(
                    schemas.FileBase(
                        relative_path=str(file_path.relative_to(root).as_posix()),
                        suffix=file_path.suffix,
                        size=size,  
                    )
                )

        return files_tree

        
    def file_load(self, repo_path: str) -> list[schemas.RepositoryFile]:  ## 仓库的读取
        repository_files = []  
        file_path = Path(repo_path).resolve()

        if not file_path.exists():
            raise FileNotFoundError(f"Repository path '{repo_path}' does not exist.")

        if not file_path.is_file():
            raise IsADirectoryError(f"Repository path '{repo_path}' is not a file.")

        content = file_path.read_text(encoding="utf-8")
        line_count = len(content.splitlines())
        path = str(file_path)
        repositoryfile = schemas.RepositoryFile(path=path, content=content, line_count=line_count)
        
        repository_files.append(repositoryfile)
        return repository_files  ## 暂时不确定

"""
    def file_filter(self, repository_files: list[schemas.RepositoryFile]) -> dict:  ## 仓库的分析
"""
