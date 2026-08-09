from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
from jinja2 import Template
from app.configuration import logger

PROMPTS_DIR = Path(__file__).parent

STRUCTURE_OPTIONS: Dict[str, Tuple[str, str]] = {
    "Story": ("Personal story", "a narrative focusing on personal experience, journey, or moment"),
    "Learning": ("Learning & Reflection", "a thoughtful reflection on key takeaways and insights gained"),
    "Project": ("Project explanation", "a clear explanation of what was built, why, and what was learned"),
    "Career": ("Career update & Reflection", "an honest milestone update and personal career reflection"),
    "Opinion": ("Grounded perspective", "a thoughtful, balanced perspective on a tool, skill, or concept"),
    "Achievement": ("Milestone update", "a humble update on completing a goal or project"),
    "Educational": ("Breakdown & Takeaway", "a clear, accessible breakdown of an experience or topic"),
    "Personal Experience": ("Experience narrative", "a personal experience narrative focusing on real context")
}


class PromptBuilder:
    @staticmethod
    def load_template(filename: str) -> Template:
        file_path = PROMPTS_DIR / filename
        if not file_path.exists():
            logger.error(f"Prompt template file missing: {file_path}")
            raise FileNotFoundError(f"Prompt template {filename} not found")
        with open(file_path, "r", encoding="utf-8") as f:
            return Template(f.read())

    @staticmethod
    def get_system_prompt() -> str:
        template = PromptBuilder.load_template("system.txt")
        return template.render()

    @staticmethod
    def select_structure(topic: str, post_type: str = "Story") -> Tuple[str, str]:
        topic_lower = topic.lower()
        if "project" in topic_lower or "built" in topic_lower or "building" in topic_lower or "arduino" in topic_lower:
            return ("Project explanation", "a clear explanation of what was built, why, and what was learned")
        elif "learn" in topic_lower or "c++" in topic_lower or "skill" in topic_lower or "first year" in topic_lower:
            return ("Reflection & Learning", "a thoughtful reflection on the learning process and personal takeaways")
        elif "internship" in topic_lower or "career" in topic_lower or "job" in topic_lower:
            return ("Experience narrative", "a personal experience update focusing on practical growth and reflection")
        elif "hackathon" in topic_lower or "failed" in topic_lower or "failure" in topic_lower:
            return ("Problem & Realization", "a turning-point story moving from an obstacle to clarity")
        
        return STRUCTURE_OPTIONS.get(post_type, ("Personal story", "a narrative focusing on personal experience"))

    @staticmethod
    def build_generation_prompt(
        topic: str,
        post_type: str = "Story",
        tone: str = "Conversational",
        language: str = "English",
        target_audience: Optional[str] = "",
        personal_context: Optional[str] = "",
        key_points: Optional[str] = "",
        length: str = "Medium",
        writing_style: Optional[str] = "",
        style_profile: Optional[Dict[str, Any]] = None,
        structure_override: Optional[Tuple[str, str]] = None
    ) -> str:
        template = PromptBuilder.load_template("generate.txt")
        
        length_map = {
            "Short": "Short & concise (~50-80 words)",
            "Medium": "Medium length (~80-150 words)",
            "Long": "Comprehensive deep dive (~150-250 words)"
        }
        length_desc = length_map.get(length, "Medium length (~80-150 words)")

        struct_name, struct_desc = structure_override or PromptBuilder.select_structure(topic, post_type)

        return template.render(
            topic=topic,
            post_type=post_type,
            tone=tone,
            language=language or "English",
            target_audience=target_audience or "",
            length_description=length_desc,
            personal_context=personal_context or "",
            key_points=key_points or "",
            writing_style=writing_style or "",
            style_profile=style_profile,
            selected_structure_name=struct_name,
            selected_structure=struct_desc
        )

    @staticmethod
    def build_relevance_validation_prompt(
        topic: str,
        draft_content: str,
        personal_context: Optional[str] = "",
        key_points: Optional[str] = ""
    ) -> str:
        template = PromptBuilder.load_template("validate_relevance.txt")
        return template.render(
            topic=topic,
            draft_content=draft_content,
            personal_context=personal_context or "",
            key_points=key_points or ""
        )

    @staticmethod
    def build_style_analysis_prompt(samples: List[str]) -> str:
        template = PromptBuilder.load_template("analyze_style.txt")
        return template.render(samples=samples)

    @staticmethod
    def build_quality_analysis_prompt(post_content: str) -> str:
        template = PromptBuilder.load_template("analyze_quality.txt")
        return template.render(post_content=post_content)

    @staticmethod
    def build_editor_pass_prompt(
        draft_content: str,
        writing_style: Optional[str] = "",
        language: str = "English"
    ) -> str:
        template = PromptBuilder.load_template("editor_pass.txt")
        return template.render(
            draft_content=draft_content,
            writing_style=writing_style or "",
            language=language or "English"
        )

    @staticmethod
    def build_refinement_prompt(
        action_filename: str,
        current_content: str,
        additional_instructions: Optional[str] = "",
        language: str = "English"
    ) -> str:
        template = PromptBuilder.load_template(action_filename)
        return template.render(
            current_content=current_content,
            additional_instructions=additional_instructions or "",
            language=language or "English"
        )
