# 项目架构
## 1. 项目目标
- 前期是一个可以帮助用户对开源项目或者本地项目进行分析，解答用户问题的ai协作平台，功能有问题解析、子问题拆分、仓库内容分析、代码分块、关键代码筛查、资料总结、问题回答
- 后期则进行功能拓展升级，转化为协助用户进行仓库维护的ai平台，功能基于前期功能，新增issue分类、issue分析等（后续添加）

## 2. 第一版（是否完成：否）
### 实现内容
- 用户输入
- 目录树扫描（先对无用的目录进行过滤，再返回完整有用目录）
- 项目内容读取
- 文件过滤
- 代码切分
- 操作执行
- 工具调用
- llm回答
- 文件/资料来源注明
- 异常处理

### 功能
- 分析项目
- 解答问题

### 目录树
见word文件

### 备忘录
- 第一版工具、skill等统一写到services里
- llm在判断文件是否足够时，可以写个循环
- token数、读取.gitignore
- 后续目录扫描可以参考gitingest、增加用户自己添加应该忽略文件的功能
- 推荐让用户在创建配置时传入额外规则，避免代码运行到一半时配置突然改变

### 进度
- **已完成：**
1. 完成了文件加载函数（load（在D:\github-assitant\services\repo_analyzer.py）），定义了RepositoryFile类（在schemas.py里）
2. 完成了应该过滤的文件的配置与其测试
3. 完成了目录树扫描功能与其测试

- **正在进行：**


## 3. 核心模块
- GithubAssistant：收集所有skill、属性等，统筹流程
- RepoAnalyse：调动项目分析流程
- FileSelector：过滤文件
- CodeChunker：切分代码
- KeywordRetriever：相关代码或文件片段筛查
- ContextBuilder：组织上下文（此模块也要进行资料/代码来源的整理）
- LLMProvider：调用模型
- QuestionAnswer：生成答案

## 4. 整体流程
   用户输入
-> GithubAssistant创建
-> 用户调用RepoAnalyse收集内容
-> RepoAnalyse内调用FileSelector
-> CodeChunker
-> KeywordRetriever
-> ContextBuilder
-> LLMProvider
-> 生成答案

## 5. 目录树

