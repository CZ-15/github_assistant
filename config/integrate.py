'''
先在config.py里写默认配置格式转化函数（自定义配置就在yaml里面统一写好，不用额外转换格式了），
统一下格式， 然后把他们两个传进合并函数，合并函数里先读取自定义配置里jinja模板内容，然后进行渲染，最后合并。
'''
from config.default import Config as DefaultConfig
from jinja2 import Environment, StrictUndefined
from pathlib import Path
import yaml
from copy import deepcopy
from typing import Any


def load_default_config() -> dict:
    defaults = DefaultConfig()
    return {
        "ignored" : {
            "directories" : defaults.DEFAULT_IGNORED_DIRECTORIES,
            "files" : defaults.DEFAULT_IGNORED_FILES,
            "suffixes" : defaults.DEFAULT_IGNORED_SUFFIXES
        },

        "agent" : {
            "cost_limit" : defaults.cost_limit,
            "step_limit" : defaults.step_limit,
            "max_retries" : defaults.max_retries,
            "timeout" : defaults.timeout,
            "max_consecutive_errors" : defaults.max_consecutive_errors,
        },
        "model" : {
            "name" : defaults.model_name,
            "provider" : defaults.model_provider,
            "temperature" : defaults.model_temperature
        }
    }


def render_user_config(user_path: str, template_values: dict) -> str:  # 渲染返回用户自定义配置
    user_path = Path(user_path)
    template_text = user_path.read_text(encoding = "utf-8")

    environment = Environment(
        undefined=StrictUndefined,
        autoescape=False,
    )

    template = environment.from_string(template_text)

    rendered_text = template.render(**template_values)

    return rendered_text


def user_text_load(rendered_text: str) -> dict:  # 转为python对象
    user_config = yaml.safe_load(rendered_text)

    if user_config is None:
        return {}
    
    if not isinstance(user_config, dict):
        raise TypeError(
            "用户配置顶层必须是字典"
        )

    return user_config


def merge(user: dict, default: dict) -> dict:
    '''
    先深拷贝一个result，然后在result上进行修改。采用反复调用的方法从内到外进行修改
    '''
    result = deepcopy(default)

    for user_key, user_value in user.items():
        if user_value is None:
            continue

        default_value = result.get(user_key)

        if (
            isinstance(default_value, dict)
            and isinstance(user_value, dict)
        ):
            result[user_key] = merge(user_value, default_value)
        else:
            result[user_key] = deepcopy(user_value)

    return result


def specific_merge(default: dict, user: dict) -> dict:
    result = merge(user, default)

    ignored_default = default.get("ignored", {})
    ignored_user = user.get("ignored", {})

    if ignored_user is None:
        ignored_user = {}

    for key in ["directories", "files", "suffixes"]:
        default_values = ignored_default.get(key) or []
        user_values = ignored_user.get(key) or []

        result["ignored"][key] = (
            frozenset(default_values)
            | frozenset(user_values)
        )

    return result


class AppConfig:
    def __init__(self, config_data: dict[str, Any]) -> dict:
        self._data = deepcopy(config_data)

        agent = self._data["aegnt"]
        model = self._data["model"]
        ignored = self._data["ignored"]

        self.IGNORED_DIRECTORIES = ignored["directories"]
        self.IGNORED_FILES = ignored["files"]
        self.IGNORED_SUFFIXES = ignored["suffixes"]

        self.cost_limit = agent["cost_limit"]
        self.step_limit = agent["step_limit"]
        self.max_retries = agent["max_retries"]
        self.timeout = agent["timeout"]
        self.max_consecutive_errors = (
            agent["max_consecutive_errors"]
        )

        self.model_name = model["name"]
        self.model_provider = model["provider"]
        self.model_temperature = (
            model["temperature"]
        )


    @property
    def data(self) -> dict[str, Any]:
        return deepcopy(self._data)

    


    
