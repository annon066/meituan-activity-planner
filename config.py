"""配置管理"""
import os
import json
from pathlib import Path

_project_root = Path(__file__).parent

# 支持 .env 文件加载
_env_file = _project_root / ".env"
if _env_file.exists():
    for line in _env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())

LLM_BASE_URL = os.environ.get("LLM_BASE_URL", "")
LLM_API_KEY = os.environ.get("LLM_API_KEY", "")
LLM_MODEL = os.environ.get("LLM_MODEL", "DeepSeek-V4-Flash")
SSL_VERIFY = os.environ.get("SSL_VERIFY", "1") != "0"

# config_local.json 优先级最高（由 Web UI 写入，持久化用户配置）
_config_local_file = _project_root / "config_local.json"
if _config_local_file.exists():
    try:
        _local = json.loads(_config_local_file.read_text())
        if _local.get("base_url"):
            LLM_BASE_URL = _local["base_url"]
        if _local.get("api_key"):
            LLM_API_KEY = _local["api_key"]
        if _local.get("model"):
            LLM_MODEL = _local["model"]
    except (json.JSONDecodeError, OSError):
        pass
