import json
from typing import List, Dict, Any, Optional
from sqlalchemy import select, delete, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.history import HistoryItem
from app.schemas.post import GenerateRequest, RefineRequest, PostResponse
from app.configuration import logger


class HistoryService:
    @staticmethod
    async def create_from_generation(
        req: GenerateRequest,
        response: PostResponse,
        db: AsyncSession
    ) -> Optional[HistoryItem]:
        logger.info("[History] Saving generated post")
        logger.info(f"[History] Save request started for topic='{req.topic}'")
        try:
            meta = response.metadata or {}
            item = HistoryItem(
                topic=req.topic,
                post_type=req.post_type,
                tone=req.tone,
                target_audience=req.target_audience or "",
                language=req.language,
                writing_style=req.writing_style or "",
                personal_context=req.personal_context or "",
                key_points=req.key_points or "",
                length=req.length,
                post=response.post,
                word_count=meta.get("word_count", 0),
                reading_time=meta.get("reading_time", "1 min read"),
                emoji_count=meta.get("emoji_count", 0),
                hashtag_count=meta.get("hashtag_count", 0),
                action=meta.get("action", "generate"),
                metadata_json=json.dumps(meta)
            )
            db.add(item)
            await db.commit()
            await db.refresh(item)
            logger.info(f"[History] Save successful. History ID='{item.id}' for topic='{req.topic}'")
            return item
        except Exception as e:
            logger.error(f"[History] Save failed: {e}", exc_info=True)
            await db.rollback()
            return None

    @staticmethod
    async def create_from_refinement(
        req: RefineRequest,
        action_name: str,
        response: PostResponse,
        db: AsyncSession,
        parent_id: Optional[str] = None,
        original_topic: Optional[str] = None,
        post_type: str = "Story",
        tone: str = "Conversational",
        target_audience: str = "",
        writing_style: str = "",
        **kwargs
    ) -> Optional[HistoryItem]:
        logger.info(f"[History] Saving refined post (action='{action_name}')")
        logger.info(f"[History] Save request started for action='{action_name}'")
        try:
            meta = response.metadata or {}
            topic_str = original_topic or "Refined Post"
            item = HistoryItem(
                topic=topic_str,
                post_type=post_type,
                tone=tone,
                target_audience=target_audience,
                language=req.language or "English",
                writing_style=writing_style,
                post=response.post,
                word_count=meta.get("word_count", 0),
                reading_time=meta.get("reading_time", "1 min read"),
                emoji_count=meta.get("emoji_count", 0),
                hashtag_count=meta.get("hashtag_count", 0),
                action=action_name,
                parent_id=parent_id,
                metadata_json=json.dumps(meta)
            )
            db.add(item)
            await db.commit()
            await db.refresh(item)
            logger.info(f"[History] Save successful. History ID='{item.id}' (action='{action_name}')")
            return item
        except Exception as e:
            logger.error(f"[History] Save failed: {e}", exc_info=True)
            await db.rollback()
            return None

    @staticmethod
    async def get_all(
        db: AsyncSession,
        q: Optional[str] = None,
        language: Optional[str] = None,
        post_type: Optional[str] = None,
        limit: int = 100,
        skip: int = 0
    ) -> List[Dict[str, Any]]:
        stmt = select(HistoryItem).order_by(HistoryItem.created_at.desc())

        filters = []
        if q and q.strip():
            query_str = f"%{q.strip()}%"
            filters.append(
                or_(
                    HistoryItem.topic.ilike(query_str),
                    HistoryItem.post.ilike(query_str),
                    HistoryItem.language.ilike(query_str),
                    HistoryItem.post_type.ilike(query_str)
                )
            )
        if language and language.strip() and language.strip().lower() != "all":
            filters.append(HistoryItem.language.ilike(language.strip()))

        if post_type and post_type.strip() and post_type.strip().lower() != "all":
            filters.append(HistoryItem.post_type.ilike(post_type.strip()))

        if filters:
            stmt = stmt.where(*filters)

        stmt = stmt.offset(skip).limit(limit)
        result = await db.execute(stmt)
        items = result.scalars().all()
        return [item.to_dict() for item in items]

    @staticmethod
    async def get_by_id(db: AsyncSession, history_id: str) -> Optional[Dict[str, Any]]:
        stmt = select(HistoryItem).where(HistoryItem.id == history_id)
        result = await db.execute(stmt)
        item = result.scalar_one_or_none()
        return item.to_dict() if item else None

    @staticmethod
    async def delete_by_id(db: AsyncSession, history_id: str) -> bool:
        stmt = select(HistoryItem).where(HistoryItem.id == history_id)
        result = await db.execute(stmt)
        item = result.scalar_one_or_none()
        if not item:
            return False
        await db.delete(item)
        await db.commit()
        return True

    @staticmethod
    async def clear_all(db: AsyncSession) -> int:
        stmt = delete(HistoryItem)
        result = await db.execute(stmt)
        await db.commit()
        return result.rowcount or 0
