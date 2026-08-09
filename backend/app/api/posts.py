from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.post import Post, PostVersion
from app.schemas.post import (
    PostGenerateRequest,
    PostRefineRequest,
    PostOut,
    PostVersionOut
)
from app.services.generation import GenerationService
from app.services.refinement import RefinementService

router = APIRouter(prefix="/posts", tags=["Posts"])


def format_post_out(post: Post) -> PostOut:
    latest_v = next((v for v in post.versions if v.version == post.latest_version), None)
    if not latest_v and post.versions:
        latest_v = post.versions[-1]

    current_content = latest_v.content if latest_v else ""
    word_count = latest_v.word_count if latest_v else 0

    return PostOut(
        id=post.id,
        topic=post.topic,
        post_type=post.post_type,
        tone=post.tone,
        personal_context=post.personal_context,
        key_points=post.key_points,
        length=post.length,
        latest_version=post.latest_version,
        current_content=current_content,
        word_count=word_count,
        created_at=post.created_at,
        updated_at=post.updated_at,
        versions=[PostVersionOut.model_validate(v) for v in post.versions]
    )


@router.post("/generate", response_model=PostOut, status_code=status.HTTP_201_CREATED)
async def generate_post(
    req: PostGenerateRequest,
    db: AsyncSession = Depends(get_db)
):
    post = await GenerationService.generate_post(req, db)
    # Reload with versions relationship
    stmt = select(Post).options(selectinload(Post.versions)).where(Post.id == post.id)
    result = await db.execute(stmt)
    full_post = result.scalar_one()
    return format_post_out(full_post)


@router.post("/{post_id}/refine", response_model=PostOut)
async def refine_post(
    post_id: str,
    req: PostRefineRequest,
    db: AsyncSession = Depends(get_db)
):
    await RefinementService.refine_post(post_id, req, db)
    stmt = select(Post).options(selectinload(Post.versions)).where(Post.id == post_id)
    result = await db.execute(stmt)
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return format_post_out(post)


@router.get("/{post_id}", response_model=PostOut)
async def get_post(
    post_id: str,
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Post).options(selectinload(Post.versions)).where(Post.id == post_id)
    result = await db.execute(stmt)
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return format_post_out(post)


@router.get("", response_model=List[PostOut])
async def list_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    stmt = (
        select(Post)
        .options(selectinload(Post.versions))
        .order_by(Post.updated_at.desc())
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    posts = result.scalars().all()
    return [format_post_out(p) for p in posts]


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: str,
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Post).where(Post.id == post_id)
    result = await db.execute(stmt)
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    await db.delete(post)
    await db.commit()
    return None
