import toml
from pathlib import Path

class Config:
    def __init__(self, config_path: str = "config.toml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self):
        if not self.config_path.exists():
            raise FileNotFoundError(f"配置文件不存在: {self.config_path}")
        return toml.load(self.config_path)
    
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
    
    def get(self, key, default=None):
        return self.config.get(key, default)

config = Config()
