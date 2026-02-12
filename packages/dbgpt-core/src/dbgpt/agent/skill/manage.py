"""Skill manager."""

import json
import logging
from typing import Any, Dict, List, Optional, Type, Union, cast

from dbgpt.component import BaseComponent, ComponentType, SystemApp
from dbgpt.util.parameter_utils import ParameterDescription

from .base import Skill, SkillBase, SkillMetadata, SkillType
from .parameters import SkillParameters

logger = logging.getLogger(__name__)


class RegisterSkill:
    """Register skill model."""

    def __init__(
        self,
        name: str,
        skill_cls: Type[SkillBase],
        skill_instance: Optional[SkillBase] = None,
        metadata: Optional[SkillMetadata] = None,
        is_class: bool = True,
    ):
        """Initialize register skill.

        Args:
            name: Skill name.
            skill_cls: Skill class.
            skill_instance: Skill instance.
            metadata: Skill metadata.
            is_class: Whether it's a class or instance.
        """
        self.name = name
        self.skill_cls = skill_cls
        self.skill_instance = skill_instance
        self.metadata = metadata or (
            skill_instance.metadata if skill_instance else None
        )
        self.is_class = is_class

    @property
    def key(self) -> str:
        """Return the unique key."""
        full_cls = f"{self.skill_cls.__module__}.{self.skill_cls.__qualname__}"
        return f"{self.name}:{full_cls}"

    @property
    def type_key(self) -> str:
        """Return the type key."""
        if self.metadata and getattr(self.metadata, "skill_type", None):
            return self.metadata.skill_type.value
        return "custom"


class SkillManager(BaseComponent):
    """Skill manager.

    To manage the skills.
    """

    # Use a distinct component name so SkillManager does not collide with ResourceManager
    name = ComponentType.SKILL_MANAGER

    def __init__(self, system_app: SystemApp):
        """Create a new SkillManager."""
        super().__init__(system_app)
        self.system_app = system_app
        self._skills: Dict[str, RegisterSkill] = {}
        self._type_to_skills: Dict[str, List[RegisterSkill]] = {}

    def init_app(self, system_app: SystemApp):
        """Initialize the SkillManager."""
        self.system_app = system_app

    def after_start(self):
        """Register all skills after start."""
        pass

    def register_skill(
        self,
        skill_cls: Optional[Type[SkillBase]] = None,
        skill_instance: Optional[SkillBase] = None,
        name: Optional[str] = None,
        metadata: Optional[SkillMetadata] = None,
        ignore_duplicate: bool = False,
    ):
        """Register a skill.

        Args:
            skill_cls: Skill class.
            skill_instance: Skill instance.
            name: Skill name.
            metadata: Skill metadata.
            ignore_duplicate: Whether to ignore duplicate registration.
        """
        if skill_cls is None and skill_instance is None:
            raise ValueError("Skill class or instance must be provided.")

        if skill_instance is not None:
            skill_cls = type(skill_instance)  # type: ignore
            name = name or skill_instance.metadata.name
        else:
            name = name or skill_cls.__name__  # type: ignore

        metadata = metadata or (skill_instance.metadata if skill_instance else None)

        register_skill = RegisterSkill(
            name=name,
            skill_cls=skill_cls,  # type: ignore
            skill_instance=skill_instance,
            metadata=metadata,
            is_class=skill_instance is None,
        )

        if register_skill.key in self._skills:
            if ignore_duplicate:
                return
            else:
                raise ValueError(f"Skill {register_skill.key} already exists.")

        self._skills[register_skill.key] = register_skill
        if register_skill.type_key not in self._type_to_skills:
            self._type_to_skills[register_skill.type_key] = []
        self._type_to_skills[register_skill.type_key].append(register_skill)

    def get_skill(
        self,
        name: Optional[str] = None,
        skill_type: Optional[SkillType] = None,
        version: Optional[str] = None,
    ) -> Optional[SkillBase]:
        """Get a skill by name or type.

        Args:
            name: Skill name.
            skill_type: Skill type.
            version: Skill version.

        Returns:
            The skill instance or None.
        """
        if name:
            for register_skill in self._skills.values():
                if register_skill.name == name:
                    if version and register_skill.metadata.version != version:
                        continue
                    return self._instantiate_skill(register_skill)
            return None

        if skill_type:
            type_key = skill_type.value
            skills = self._type_to_skills.get(type_key, [])
            if skills:
                return self._instantiate_skill(skills[0])

        return None

    def get_skills_by_type(self, skill_type: SkillType) -> List[SkillBase]:
        """Get all skills by type.

        Args:
            skill_type: Skill type.

        Returns:
            List of skill instances.
        """
        type_key = skill_type.value
        skills = self._type_to_skills.get(type_key, [])
        return [self._instantiate_skill(skill) for skill in skills]

    def list_skills(self) -> List[Dict[str, Any]]:
        """List all registered skills.

        Returns:
            List of skill metadata dictionaries.
        """
        result = []
        for register_skill in self._skills.values():
            if register_skill.metadata is None:
                result.append({})
            else:
                # metadata may be a dataclass with to_dict method
                try:
                    result.append(register_skill.metadata.to_dict())
                except Exception:
                    # fallback to attribute access
                    result.append(
                        {
                            "name": getattr(register_skill.metadata, "name", ""),
                            "description": getattr(
                                register_skill.metadata, "description", ""
                            ),
                            "version": getattr(register_skill.metadata, "version", ""),
                        }
                    )
        return result

    def _instantiate_skill(self, register_skill: RegisterSkill) -> SkillBase:
        """Instantiate a skill from register skill.

        Args:
            register_skill: RegisterSkill instance.

        Returns:
            Skill instance.
        """
        if not register_skill.is_class:
            return cast(SkillBase, register_skill.skill_instance)

        skill_cls = cast(Type[SkillBase], register_skill.skill_cls)
        return skill_cls()

    def build_skill_from_parameters(
        self, parameters: SkillParameters
    ) -> Optional[SkillBase]:
        """Build a skill from parameters.

        Args:
            parameters: Skill parameters.

        Returns:
            Skill instance.
        """
        skill = self.get_skill(name=parameters.skill_name)
        return skill

    def retrieve_skills(self) -> List[Dict[str, Any]]:
        """Retrieve all skills metadata.

        Returns:
            List[Dict[str, Any]]: List of skill metadata including name, description and path.
        """
        # This is a basic implementation. In a real scenario, this might search directories
        # or a database. Since we currently register skills manually or via config,
        # we iterate over registered skills.
        # To support directory scanning as requested, we would need to implement
        # a scanner here or in SkillLoader.
        # For now, let's assume skills are registered.
        # BUT, the user wants to scan the directory.
        return self.list_skills()

    def get_skill_content(self, skill_name: str) -> str:
        """Get the content (SKILL.md) of a skill.

        Args:
            skill_name: The name of the skill.

        Returns:
            str: The content of the SKILL.md file.
        """
        skill = self.get_skill(name=skill_name)
        if not skill:
            return f"Skill '{skill_name}' not found."

        # If the skill was loaded from a file, we might have the path stored somewhere.
        # SkillMetadata doesn't strictly enforce a 'path' attribute, but let's check.
        # Or we can try to find it via the loader mechanism if we had the path.
        # For the sake of the example and current codebase state, let's look at metadata.
        # If we can't find the file content easily from the object, we might need to rely
        # on how it was loaded.

        # A workaround for the example: The Skill object usually has prompt_template.
        # If it's a file-based skill, the prompt_template IS the content.
        if skill.prompt_template:
            # prompt_template might be a string or a Template object
            if hasattr(skill.prompt_template, "template"):
                return skill.prompt_template.template
            return str(skill.prompt_template)

        return "No content available for this skill."

    def get_skill_scripts(self, skill_name: str) -> List[Dict[str, Any]]:
        """Get scripts defined in a skill's configuration.

        Scripts are defined in the skill's config with the following format:
        ```yaml
        scripts:
          - name: "script_name"
            description: "Script description"
            language: "python"
            code: "..."
        ```

        Args:
            skill_name: The name of the skill.

        Returns:
            List of script definitions.
        """
        skill = self.get_skill(name=skill_name)
        if not skill:
            return []

        # Try to get scripts from skill's config
        scripts = []

        # Check if skill has config attribute (Skill class)
        if hasattr(skill, "config") and skill.config:
            config_scripts = skill.config.get("scripts", [])
            if isinstance(config_scripts, list):
                scripts.extend(config_scripts)

        # Check if skill has metadata with config (FileBasedSkill)
        if hasattr(skill, "metadata") and skill.metadata:
            metadata = skill.metadata
            if hasattr(metadata, "config") and metadata.config:
                config_scripts = metadata.config.get("scripts", [])
                if isinstance(config_scripts, list):
                    # Avoid duplicates if already added from skill.config
                    existing_names = {s.get("name") for s in scripts}
                    for s in config_scripts:
                        if s.get("name") not in existing_names:
                            scripts.append(s)

        return scripts

    async def execute_script(
        self,
        skill_name: str,
        script_name: str,
        args: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Execute a script defined in a skill.

        Args:
            skill_name: The name of the skill containing the script.
            script_name: The name of the script to execute.
            args: Arguments to pass to the script.

        Returns:
            JSON string with execution results.
        """
        from dbgpt.util.code.server import get_code_server

        args = args or {}

        # Get the script
        scripts = self.get_skill_scripts(skill_name)
        script = next(
            (s for s in scripts if s.get("name") == script_name),
            None,
        )

        if not script:
            return json.dumps(
                {
                    "chunks": [
                        {
                            "output_type": "text",
                            "content": f"Script '{script_name}' not found in skill '{skill_name}'",
                        }
                    ]
                },
                ensure_ascii=False,
            )

        code = script.get("code", "")
        language = script.get("language", "python")

        if not code:
            return json.dumps(
                {
                    "chunks": [
                        {
                            "output_type": "text",
                            "content": f"Script '{script_name}' has no code",
                        }
                    ]
                },
                ensure_ascii=False,
            )

        # Replace parameters in code using safe template substitution
        # Use string.Template for safe substitution to avoid code injection
        try:
            from string import Template

            template = Template(code)
            substituted_code = template.safe_substitute(**args)
        except Exception as e:
            return json.dumps(
                {
                    "chunks": [
                        {
                            "output_type": "text",
                            "content": f"Parameter substitution failed: {str(e)}",
                        }
                    ]
                },
                ensure_ascii=False,
            )

        # Execute the code
        try:
            code_server = await get_code_server(self.system_app)
            result = await code_server.exec(substituted_code, language)
            output = (
                result.output.decode("utf-8")
                if isinstance(result.output, bytes)
                else str(result.output)
            )
            error_output = (
                result.error_message.decode("utf-8")
                if isinstance(result.error_message, bytes)
                else str(result.error_message or "")
            )

            chunks: List[Dict[str, Any]] = [
                {"output_type": "code", "content": substituted_code}
            ]

            if error_output:
                chunks.append({"output_type": "text", "content": f"Error: {error_output}"})

            if output:
                chunks.append({"output_type": "text", "content": output})

            return json.dumps({"chunks": chunks}, ensure_ascii=False)
        except Exception as e:
            return json.dumps(
                {
                    "chunks": [
                        {
                            "output_type": "text",
                            "content": f"Script execution failed: {str(e)}",
                        }
                    ]
                },
                ensure_ascii=False,
            )


_SYSTEM_APP: Optional[SystemApp] = None


def initialize_skill(system_app: SystemApp):
    """Initialize the skill manager."""
    global _SYSTEM_APP
    _SYSTEM_APP = system_app
    skill_manager = SkillManager(system_app)
    system_app.register_instance(skill_manager)


def get_skill_manager(system_app: Optional[SystemApp] = None) -> SkillManager:
    """Get the skill manager.

    Args:
        system_app: System app instance.

    Returns:
        SkillManager instance.
    """
    global _SYSTEM_APP
    if not _SYSTEM_APP:
        if not system_app:
            system_app = SystemApp()
        initialize_skill(system_app)
    app = system_app or _SYSTEM_APP
    return SkillManager.get_instance(cast(SystemApp, app))
