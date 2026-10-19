from pydantic import BaseModel, Field


class RepositoryFile(BaseModel):  ## 仓库文件对象
    path: str
    content: str
    line_count: int


class FileBase(BaseModel):  ## 目录树扫描后的结果
    relative_path: str
    suffix: str  ## 文件后缀
    size: int = Field(ge = 0)  ## 文件大小