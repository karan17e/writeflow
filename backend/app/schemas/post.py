from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any


class QualityAnalyzeRequest(BaseModel):
    post: str = Field(..., min_length=5, description="The post content to analyze")
    provider: Optional[str] = Field(default=None, description="LLM provider override")


class StyleAnalyzeRequest(BaseModel):
    samples: List[str] = Field(..., min_length=1, max_length=5, description="1 to 5 writing samples")
    provider: Optional[str] = Field(default=None, description="LLM provider override")


class GenerateRequest(BaseModel):
    topic: str = Field(..., min_length=1, description="Topic or main idea of the post")
    post_type: str = Field(default="Story", description="Type of post: Achievement, Project, Learning, Career, Opinion, Story, Educational, Personal Experience")
    tone: str = Field(default="Conversational", description="Tone of voice: Professional, Conversational, Casual, Confident, Thoughtful, Storytelling")
    language: str = Field(default="English", description="Language of the generated post: English, Hindi, Hinglish")
    target_audience: Optional[str] = Field(default="", description="Target audience for the post")
    personal_context: Optional[str] = Field(default="", description="Personal experience or context to weave in")
    key_points: Optional[str] = Field(default="", description="Key points to include in the post")
    length: str = Field(default="Medium", description="Post length: Short, Medium, Long")
    writing_style: Optional[str] = Field(default="", description="User's personal writing style preferences")
    writing_samples: Optional[List[str]] = Field(default=[], description="User's 1-5 writing samples")
    style_profile: Optional[Dict[str, Any]] = Field(default=None, description="Pre-computed style profile JSON")
    provider: Optional[str] = Field(default=None, description="LLM provider override")

    @field_validator("topic", mode="before")
    @classmethod
    def validate_topic(cls, v: Any) -> str:
        if not v or not str(v).strip():
            raise ValueError("Topic cannot be empty.")
        return str(v).strip()

    @field_validator("language", mode="before")
    @classmethod
    def validate_language(cls, v: Any) -> str:
        if not v or not str(v).strip():
            return "English"
        val = str(v).strip()
        val_cap = val.capitalize()
        allowed = {"English", "Hindi", "Hinglish"}
        if val_cap in allowed:
            return val_cap
        if val not in allowed:
            raise ValueError(f"Language must be one of: {', '.join(sorted(allowed))}")
        return val

    @field_validator("target_audience", "personal_context", "key_points", "writing_style", mode="before")
    @classmethod
    def validate_optional_strings(cls, v: Any) -> str:
        if v is None:
            return ""
        return str(v)

    @field_validator("writing_samples", mode="before")
    @classmethod
    def validate_writing_samples(cls, v: Any) -> List[str]:
        if v is None:
            return []
        if isinstance(v, list):
            return [str(s).strip() for s in v if s and str(s).strip()]
        return []


class RefineRequest(BaseModel):
    post: str = Field(..., min_length=5, description="The existing post content to refine")
    additional_instructions: Optional[str] = Field(default="", description="Optional additional instructions")
    language: Optional[str] = Field(default="English", description="Language of the post: English, Hindi, Hinglish")
    provider: Optional[str] = Field(default=None, description="LLM provider override")

    @field_validator("language", mode="before")
    @classmethod
    def validate_refine_language(cls, v: Any) -> str:
        if not v or not str(v).strip():
            return "English"
        val = str(v).strip()
        allowed = {"English", "Hindi", "Hinglish"}
        if val not in allowed:
            return "English"
        return val


class PostResponse(BaseModel):
    post: str
    metadata: Dict[str, Any]
