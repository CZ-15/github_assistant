from pydantic import BaseModel


class RepositoryFile(BaseModel):  ## 仓库文件对象
    path: str
    content: str
    line_count: int