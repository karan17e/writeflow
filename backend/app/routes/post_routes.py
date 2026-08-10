from typing import Dict, Any
from fastapi import APIRouter, HTTPException, status
from app.schemas.post import (
    GenerateRequest,
    RefineRequest,
    PostResponse,
    StyleAnalyzeRequest,
    QualityAnalyzeRequest
)
from app.services.post_service import PostService
from app.configuration import logger

router = APIRouter(tags=["WriteFlow Posts"])


@router.post("/generate", response_model=PostResponse, status_code=status.HTTP_200_OK)
async def generate_post(req: GenerateRequest):
    logger.info(f"BACKEND REQUEST RECEIVED: topic='{req.topic}', [WriteFlow] Selected language: {req.language}, provider='{req.provider or 'default'}'")
    try:
        return await PostService.generate_post(req)
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
async def rewrite_post(req: RefineRequest):
    logger.info("BACKEND REQUEST RECEIVED: /api/rewrite")
    try:
        return await PostService.rewrite_post(req)
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
async def improve_hook(req: RefineRequest):
    logger.info("BACKEND REQUEST RECEIVED: /api/improve-hook")
    try:
        return await PostService.improve_hook(req)
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
async def humanize_post(req: RefineRequest):
    logger.info("BACKEND REQUEST RECEIVED: /api/humanize")
    try:
        return await PostService.humanize_post(req)
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
async def shorten_post(req: RefineRequest):
    logger.info("BACKEND REQUEST RECEIVED: /api/shorten")
    try:
        return await PostService.shorten_post(req)
    except ValueError as ve:
        logger.error(f"Configuration error in shorten_post: {str(ve)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        logger.exception("Failed to shorten post")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while shortening the post: {str(e)}"
        )
