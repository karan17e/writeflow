from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.post import (
    GenerateRequest,
    RefineRequest,
    PostResponse,
    StyleAnalyzeRequest,
    QualityAnalyzeRequest
)
from app.services.post_service import PostService
from app.services.history_service import HistoryService
from app.configuration import logger

router = APIRouter(tags=["WriteFlow Posts"])


@router.post("/generate", response_model=PostResponse, status_code=status.HTTP_200_OK)
async def generate_post(req: GenerateRequest, db: AsyncSession = Depends(get_db)):
    logger.info(f"BACKEND REQUEST RECEIVED: topic='{req.topic}', [WriteFlow] Selected language: {req.language}, provider='{req.provider or 'default'}'")
    try:
        response = await PostService.generate_post(req)
        # Automatic background DB save
        item = await HistoryService.create_from_generation(req, response, db)
        if item:
            response.metadata["history_id"] = item.id
        return response
    except ValueError as ve:
        logger.error(f"Configuration or validation error in generate_post: {str(ve)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to generate your post. ({str(ve)})"
        )
    except Exception as e:
        err_msg = str(e)
        logger.exception("Failed to generate post")
        if "429" in err_msg or "rate_limit_exceeded" in err_msg or "Rate limit" in err_msg:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="AI generation is temporarily rate limited. Please try again after the provider's limit resets."
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AI generation service is temporarily unavailable. Please try again in a few moments."
        )


@router.get("/history", response_model=List[Dict[str, Any]], status_code=status.HTTP_200_OK)
async def list_history(
    q: Optional[str] = Query(None, description="Search query across topic, content, language, post_type"),
    language: Optional[str] = Query(None, description="Language filter"),
    post_type: Optional[str] = Query(None, description="Post type filter"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: AsyncSession = Depends(get_db)
):
    logger.info(f"BACKEND REQUEST RECEIVED: GET /api/history (q='{q}', language='{language}', post_type='{post_type}')")
    try:
        return await HistoryService.get_all(db, q=q, language=language, post_type=post_type, limit=limit, skip=skip)
    except Exception as e:
        logger.exception("Failed to fetch post history")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching history: {str(e)}"
        )


@router.get("/history/{history_id}", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
async def get_history_item(history_id: str, db: AsyncSession = Depends(get_db)):
    logger.info(f"BACKEND REQUEST RECEIVED: GET /api/history/{history_id}")
    item = await HistoryService.get_by_id(db, history_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="History item not found.")
    return item


@router.delete("/history/{history_id}", status_code=status.HTTP_200_OK)
async def delete_history_item(history_id: str, db: AsyncSession = Depends(get_db)):
    logger.info(f"BACKEND REQUEST RECEIVED: DELETE /api/history/{history_id}")
    success = await HistoryService.delete_by_id(db, history_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="History item not found.")
    return {"message": "History item deleted successfully.", "id": history_id}


@router.delete("/history", status_code=status.HTTP_200_OK)
async def clear_all_history(db: AsyncSession = Depends(get_db)):
    logger.info("BACKEND REQUEST RECEIVED: DELETE /api/history (Clear All)")
    count = await HistoryService.clear_all(db)
    return {"message": f"Successfully deleted {count} history items.", "deleted_count": count}


@router.post("/analyze", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
async def analyze_quality(req: QualityAnalyzeRequest):
    logger.info("BACKEND REQUEST RECEIVED: /api/analyze")
    try:
        return await PostService.analyze_quality(req, provider_name=req.provider)
    except ValueError as ve:
        logger.error(f"Configuration or validation error in analyze_quality: {str(ve)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        logger.exception("Failed to analyze post quality")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while analyzing post quality: {str(e)}"
        )


@router.post("/analyze-style", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
async def analyze_style(req: StyleAnalyzeRequest):
    logger.info("BACKEND REQUEST RECEIVED: /api/analyze-style")
    try:
        return await PostService.analyze_style(req, provider_name=req.provider)
    except ValueError as ve:
        logger.error(f"Configuration or validation error in analyze_style: {str(ve)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        logger.exception("Failed to analyze writing style")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while analyzing writing style: {str(e)}"
        )


@router.post("/rewrite", response_model=PostResponse, status_code=status.HTTP_200_OK)
async def rewrite_post(req: RefineRequest, db: AsyncSession = Depends(get_db)):
    logger.info("BACKEND REQUEST RECEIVED: /api/rewrite")
    try:
        response = await PostService.rewrite_post(req)
        item = await HistoryService.create_from_refinement(req, "rewrite", response, db)
        if item:
            response.metadata["history_id"] = item.id
        return response
    except ValueError as ve:
        logger.error(f"Configuration error in rewrite_post: {str(ve)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        logger.exception("Failed to rewrite post")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while rewriting the post: {str(e)}"
        )


@router.post("/improve-hook", response_model=PostResponse, status_code=status.HTTP_200_OK)
async def improve_hook(req: RefineRequest, db: AsyncSession = Depends(get_db)):
    logger.info("BACKEND REQUEST RECEIVED: /api/improve-hook")
    try:
        response = await PostService.improve_hook(req)
        item = await HistoryService.create_from_refinement(req, "improve_hook", response, db)
        if item:
            response.metadata["history_id"] = item.id
        return response
    except ValueError as ve:
        logger.error(f"Configuration error in improve_hook: {str(ve)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        logger.exception("Failed to improve hook")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while improving the hook: {str(e)}"
        )


@router.post("/humanize", response_model=PostResponse, status_code=status.HTTP_200_OK)
async def humanize_post(req: RefineRequest, db: AsyncSession = Depends(get_db)):
    logger.info("BACKEND REQUEST RECEIVED: /api/humanize")
    try:
        response = await PostService.humanize_post(req)
        item = await HistoryService.create_from_refinement(req, "humanize", response, db)
        if item:
            response.metadata["history_id"] = item.id
        return response
    except ValueError as ve:
        logger.error(f"Configuration error in humanize_post: {str(ve)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        logger.exception("Failed to humanize post")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while humanizing the post: {str(e)}"
        )


@router.post("/shorten", response_model=PostResponse, status_code=status.HTTP_200_OK)
async def shorten_post(req: RefineRequest, db: AsyncSession = Depends(get_db)):
    logger.info("BACKEND REQUEST RECEIVED: /api/shorten")
    try:
        response = await PostService.shorten_post(req)
        item = await HistoryService.create_from_refinement(req, "shorten", response, db)
        if item:
            response.metadata["history_id"] = item.id
        return response
    except ValueError as ve:
        logger.error(f"Configuration error in shorten_post: {str(ve)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        logger.exception("Failed to shorten post")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while shortening the post: {str(e)}"
        )
