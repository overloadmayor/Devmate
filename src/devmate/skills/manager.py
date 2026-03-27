import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional
from ..utils.logger import logger
from ..utils.config import config


class Skill:
    def __init__(self, skill_dir: Path):
        self.skill_dir = skill_dir
        self.metadata = self._load_metadata()
        self.name = self.metadata.get("name", skill_dir.name)
        self.description = self.metadata.get("description", "")
        self.prompt_template = self._load_prompt_template()
    
    def _load_metadata(self) -> Dict:
        skill_file = self.skill_dir / "SKILL.md"
        if not skill_file.exists():
            logger.warning(f"技能文件不存在: {skill_file}")
            return {}
        
        try:
            with open(skill_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            # 解析 YAML frontmatter
            frontmatter_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
            if frontmatter_match:
                frontmatter_content = frontmatter_match.group(1)
                # 简单解析 YAML（只支持基本的 key: value 格式）
                metadata = {}
                for line in frontmatter_content.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        metadata[key.strip()] = value.strip()
                return metadata
            else:
                logger.warning(f"未找到 YAML frontmatter: {skill_file}")
                return {}
        except Exception as e:
            logger.error(f"加载技能元数据失败 {skill_file}: {e}")
            return {}
    
    def _load_prompt_template(self) -> Optional[str]:
        skill_file = self.skill_dir / "SKILL.md"
        if not skill_file.exists():
            return None
        
        try:
            with open(skill_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            # 移除 YAML frontmatter，只保留 markdown 内容
            frontmatter_match = re.match(r"^---\s*\n.*?\n---\s*\n", content, re.DOTALL)
            if frontmatter_match:
                return content[frontmatter_match.end():]
            return content
        except Exception as e:
            logger.error(f"加载技能提示词模板失败 {skill_file}: {e}")
            return None
    
    def get_prompt(self) -> str:
        # 只加载技能的名称和描述，不加载完整的prompt_template
        # 这样可以避免系统提示词过大
        return f"## {self.name}\n{self.description}"


class SkillsManager:
    def __init__(self):
        self.skills_dir = Path(config.skills.get("skills_dir", ".skills"))
        self.skills: Dict[str, Skill] = {}
        self._load_skills()
    
    def _load_skills(self):
        if not self.skills_dir.exists():
            logger.info(f"技能目录不存在，创建目录: {self.skills_dir}")
            self.skills_dir.mkdir(parents=True, exist_ok=True)
            return
        
        for skill_path in self.skills_dir.iterdir():
            if skill_path.is_dir():
                skill = Skill(skill_path)
                if skill.name:
                    self.skills[skill.name] = skill
                    logger.info(f"加载技能成功: {skill.name}")
    
    def get_skills_prompt(self) -> str:
        if not self.skills:
            return ""
        
        prompt = "## 可用技能\n\n"
        prompt += "以下是可用的技能列表，当你需要执行相关任务时，可以使用这些技能：\n\n"
        for skill in self.skills.values():
            prompt += f"- **{skill.name}**: {skill.description}\n"
        
        prompt += "\n当你使用技能时，请根据任务需求选择最合适的技能，并按照该技能的最佳实践来完成任务。"
        
        return prompt
    
    def get_skill(self, name: str) -> Optional[Skill]:
        return self.skills.get(name)
    
    def list_skills(self) -> List[str]:
        return list(self.skills.keys())
    
    def reload_skills(self):
        self.skills.clear()
        self._load_skills()
        logger.info("技能重新加载完成")


skills_manager = SkillsManager()
