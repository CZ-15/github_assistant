'''
先在config.py里写默认配置格式转化函数（自定义配置就在yaml里面统一写好，不用额外转换格式了），
统一下格式， 然后把他们两个传进合并函数，合并函数里先读取自定义配置里jinja模板内容，然后进行渲染，最后合并。
'''
from config.default import Config as DefaultConfig
from jinja2 import Environment, StrictUndefined
from pathlib import Path
import yaml


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


def render_user_config(user_path: str, template_values: dict) -> str:
    user_path = Path(user_path)
    template_text = user_path.read_text(encoding = "utf-8")

    environment = Environment(
        undefined=StrictUndefined,
        autoescape=False,
    )

    template = environment.from_string(template_text)

    rendered_text = template.render(**template_values)

    return rendered_text


def user_text_load(rendered_text: str) -> dict:
    user_config = yaml.safe_load(rendered_text)

    if user_config is None:
        return {}
    
    if not isinstance(user_config, dict):
        raise TypeError(
            "用户配置顶层必须是字典"
        )

    return user_config


def merge(user: dict, default: dict):
    pass

    
