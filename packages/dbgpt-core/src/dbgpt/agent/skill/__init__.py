"""Skill module for DB-GPT agent framework.

This module provides a SKILL mechanism, which allows loading and managing
agent skills that include prompts, tools, knowledge, and actions.
"""

from .agent import SkillsAgent, SkillsAgentConfig, create_skills_agent
from .base import Skill, SkillBase, SkillMetadata, SkillType
from .middleware import (
    LoadedSkill,
    SkillsMiddleware,
    _list_skills_from_directory,
    _parse_skill_metadata,
    _validate_skill_name,
)
from .middleware_v2 import SkillsMiddlewareV2
from .manage import SkillManager, get_skill_manager, initialize_skill
from .parameters import SkillParameters
from .loader import SkillLoader, SkillBuilder

__all__ = [
    "Skill",
    "SkillBase",
    "SkillMetadata",
    "SkillParameters",
    "SkillLoader",
    "SkillBuilder",
    "SkillType",
    "SkillManager",
    "get_skill_manager",
    "initialize_skill",
    "SkillsMiddleware",
    "LoadedSkill",
    "SkillsAgent",
    "SkillsAgentConfig",
    "create_skills_agent",
    "_list_skills_from_directory",
    "_parse_skill_metadata",
    "_validate_skill_name",
    "SkillsMiddlewareV2",
]
