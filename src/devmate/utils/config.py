import os
import re
import toml
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self, config_path: str = "config.toml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _replace_env_vars(self, content: str) -> str:
        pattern = re.compile(r"\$\{(\w+)\}")
        return pattern.sub(lambda m: os.getenv(m.group(1), ""), content)
    
    def _load_config(self):
        if not self.config_path.exists():
            raise FileNotFoundError(f"配置文件不存在: {self.config_path}")
        
        with open(self.config_path, "r", encoding="utf-8") as f:
            config_content = f.read()
        
        config_content = self._replace_env_vars(config_content)
        return toml.loads(config_content)
    
    @property
    def model(self):
        return self.config.get("model", {})
    
    @property
    def search(self):
        return self.config.get("search", {})
    
    @property
    def langsmith(self):
        return self.config.get("langsmith", {})
    
    @property
    def skills(self):
        return self.config.get("skills", {})

    @property
    def embedding(self):
        return self.config.get("embedding", {})

    def get(self, key, default=None):
        return self.config.get(key, default)


config = Config()
