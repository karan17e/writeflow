from pathlib import Path
from jinja2 import Template
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.models.post import Post, PostVersion
from app.schemas.post import PostRefineRequest, RefinementActionEnum
from app.llm import get_provider, LLMResponse
from app.services.generation import count_words, load_template

ACTION_TEMPERATURES = {
    RefinementActionEnum.REWRITE: 0.8,
    RefinementActionEnum.PERSONALIZE: 0.75,
    RefinementActionEnum.IMPROVE_HOOK: 0.7,
    RefinementActionEnum.SHORTEN: 0.3,
    RefinementActionEnum.REMOVE_BUZZWORDS: 0.2,
}

ACTION_TEMPLATES = {
    RefinementActionEnum.REWRITE: "rewrite.txt",
    RefinementActionEnum.PERSONALIZE: "personalize.txt",
    RefinementActionEnum.IMPROVE_HOOK: "improve_hook.txt",
    RefinementActionEnum.SHORTEN: "shorten.txt",
    RefinementActionEnum.REMOVE_BUZZWORDS: "remove_buzzwords.txt",
}


class RefinementService:
    @staticmethod
    async def refine_post(
        post_id: str,
        req: PostRefineRequest,
        db: AsyncSession
    ) -> PostVersion:
        # Fetch post
        post_stmt = select(Post).where(Post.id == post_id)
        result = await db.execute(post_stmt)
        post = result.scalar_one_or_none()

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        # Fetch latest version
        ver_stmt = select(PostVersion).where(
            PostVersion.post_id == post_id,
            PostVersion.version == post.latest_version
        )
        ver_result = await db.execute(ver_stmt)
        current_version = ver_result.scalar_one_or_none()

        if not current_version:
            raise HTTPException(status_code=404, detail="Current version of post not found")

        # Load prompts
        system_template = load_template("system.txt")
        action_template_file = ACTION_TEMPLATES[req.action]
        action_template = load_template(action_template_file)

        system_prompt = system_template.render()
        user_prompt = action_template.render(
            current_content=current_version.content,
            additional_instructions=req.additional_instructions or ""
        )

        temperature = ACTION_TEMPERATURES.get(req.action, 0.7)
        provider = get_provider(req.provider)

        llm_res: LLMResponse = await provider.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=temperature,
            max_tokens=1500
        )

        clean_content = llm_res.content.strip()
        word_count = count_words(clean_content)

        new_version_num = post.latest_version + 1
        post.latest_version = new_version_num

        new_version = PostVersion(
            post_id=post.id,
            version=new_version_num,
            content=clean_content,
            word_count=word_count,
            action=req.action.value,
            llm_provider=llm_res.provider,
            llm_model=llm_res.model
        )

        db.add(new_version)
        await db.commit()
        await db.refresh(new_version)

        return new_version
