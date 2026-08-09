import os
from pathlib import Path
from jinja2 import Template
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.post import Post, PostVersion
from app.schemas.post import PostGenerateRequest, LengthEnum
from app.llm import get_provider, LLMResponse

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def load_template(name: str) -> Template:
    path = PROMPTS_DIR / name
    with open(path, "r", encoding="utf-8") as f:
        return Template(f.read())


def count_words(text: str) -> int:
    return len(text.strip().split())


def get_length_description(length: LengthEnum) -> str:
    if length == LengthEnum.SHORT:
        return "Short & punchy (around 50 to 80 words max)"
    elif length == LengthEnum.LONG:
        return "Comprehensive & detailed (around 180 to 250 words)"
    else:
        return "Medium length (around 100 to 150 words)"


class GenerationService:
    @staticmethod
    async def generate_post(req: PostGenerateRequest, db: AsyncSession) -> Post:
        system_template = load_template("system.txt")
        generate_template = load_template("generate.txt")

        system_prompt = system_template.render()
        user_prompt = generate_template.render(
            topic=req.topic,
            post_type=req.post_type.value,
            tone=req.tone.value,
            length_description=get_length_description(req.length),
            personal_context=req.personal_context,
            key_points=req.key_points
        )

        provider = get_provider(req.provider)
        llm_res: LLMResponse = await provider.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.75,
            max_tokens=1500
        )

        clean_content = llm_res.content.strip()
        word_count = count_words(clean_content)

        # Create database records
        post = Post(
            topic=req.topic,
            post_type=req.post_type.value,
            tone=req.tone.value,
            personal_context=req.personal_context,
            key_points=req.key_points,
            length=req.length.value,
            latest_version=1
        )
        db.add(post)
        await db.flush()  # Populates post.id

        version = PostVersion(
            post_id=post.id,
            version=1,
            content=clean_content,
            word_count=word_count,
            action="generate",
            llm_provider=llm_res.provider,
            llm_model=llm_res.model
        )
        db.add(version)
        await db.commit()
        await db.refresh(post)

        return post
