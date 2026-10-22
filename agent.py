from config.config import Config
from services.repo_analyzer import RepoAnalyzer


class GithubAssistant:
    def __init__(self):
        self.cfg = Config()
        self.repo_conductor = RepoAnalyzer(self)  ## 传入self，方便RepoAnalyzer（在repo_analyzer.py中）访问GithubAssistant的属性和方法,此时repo_conductor是RepoAnalyzer的实例