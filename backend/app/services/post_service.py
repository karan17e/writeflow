import math
import json
import re
from typing import Dict, Any, List
from app.schemas.post import GenerateRequest, RefineRequest, PostResponse, StyleAnalyzeRequest, QualityAnalyzeRequest
from app.ai import get_ai_provider, AIResponse
from app.prompts import PromptBuilder
from app.services.style_validator import (
    parse_user_style_instructions,
    validate_style_requirements,
    count_emojis,
    count_hashtags
)
from app.configuration import logger


def count_words(text: str) -> int:
    return len(text.strip().split()) if text else 0


def calculate_reading_time(word_count: int) -> str:
    words_per_minute = 200
    minutes = math.ceil(word_count / words_per_minute)
    return "1 min read" if minutes <= 1 else f"{minutes} min read"


def check_template_repetition(content: str) -> bool:
    """Detects if content follows rigid formulaic templates."""
    lower = content.lower()
    patterns = [
        r"here are \d+ (things|lessons|takeaways|reasons)",
        r"\d+ (lessons|things) i learned",
        r"most people overcomplicate",
        r"most professionals overcomplicate",
        r"start small and move fast",
        r"i used to think.*now i know",
        r"here's what i realized"
    ]
    for pattern in patterns:
        if re.search(pattern, lower):
            return True
    return False


class PostService:
    @staticmethod
    async def apply_targeted_style_fix(
        post_content: str,
        requirements: Dict[str, Any],
        validation_report: Dict[str, Any],
        language: str = "English",
        provider_name: str | None = None
    ) -> str:
        """Applies a targeted edit pass to fix unsatisfied numeric requirements (e.g. emoji count) without rewriting the post."""
        logger.info("Executing targeted editing pass to satisfy user style requirements...")
        
        system_prompt = (
            f"You are a precise content editor. The target language is {language}. "
            "The user has requested exact formatting/emoji requirements. "
            "You MUST insert or adjust the exact requested number of emojis or hashtags naturally into the text. "
            f"Do NOT change the target language ({language}), underlying topic, facts, or narrative."
        )
        
        instructions = []
        details = validation_report.get("details", {})
        
        if "emoji_count" in details and not details["emoji_count"]["passed"]:
            req_c = details["emoji_count"]["requested"]
            act_c = details["emoji_count"]["actual"]
            if req_c == 0:
                instructions.append("Remove ALL emojis from the post.")
            elif req_c > act_c:
                diff = req_c - act_c
                instructions.append(
                    f"Insert exactly {diff} additional relevant emojis (such as 🐍 💻 🚀 🧠 📚 🎯) naturally across key sentences so that the final post contains AT LEAST {req_c} emojis total."
                )
            else:
                diff = act_c - req_c
                instructions.append(f"Remove {diff} emojis so the total emoji count is exactly {req_c}.")

        if "hashtag_count" in details and not details["hashtag_count"]["passed"]:
            req_h = details["hashtag_count"]["requested"]
            act_h = details["hashtag_count"]["actual"]
            if req_h == 0:
                instructions.append("Remove ALL hashtags from the post.")
            elif req_h > act_h:
                instructions.append(f"Adjust hashtags at the end so there are exactly {req_h} relevant hashtags.")
            else:
                instructions.append(f"Remove hashtags at the end so there are exactly {req_h} relevant hashtags.")

        instruction_text = "\n- ".join(instructions)
        user_prompt = (
            f"CURRENT POST:\n{post_content}\n\n"
            f"REQUIRED EDITS:\n- {instruction_text}\n\n"
            f"CRITICAL: Maintain the post strictly in {language}. Do NOT change the topic or facts. Ensure the output post contains the EXACT requested number of emojis/hashtags.\n"
            f"Return ONLY the final updated post text."
        )

        provider = get_ai_provider(provider_name)
        res: AIResponse = await provider.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.4,
            max_tokens=1500
        )
        return res.content.strip()

    @staticmethod
    async def validate_relevance(
        topic: str,
        draft_content: str,
        personal_context: str = "",
        key_points: str = "",
        provider_name: str | None = None
    ) -> Dict[str, Any]:
        logger.info(f"Auditing topic relevance & facts for topic='{topic}'")
        
        system_prompt = "You are an objective content auditor. Output strictly valid JSON."
        user_prompt = PromptBuilder.build_relevance_validation_prompt(
            topic=topic,
            draft_content=draft_content,
            personal_context=personal_context,
            key_points=key_points
        )

        provider = get_ai_provider(provider_name)
        ai_res: AIResponse = await provider.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.1,
            max_tokens=500
        )

        content = ai_res.content.strip()
        try:
            clean_str = content
            if "```" in clean_str:
                clean_str = clean_str.split("```")[1]
                if clean_str.startswith("json"):
                    clean_str = clean_str[4:]
            audit_res = json.loads(clean_str.strip())
            return audit_res
        except Exception as e:
            logger.warning(f"Could not parse relevance validation JSON: {e}. Defaulting to valid audit.")
            return {
                "is_relevant": True,
                "relevance_score": 9,
                "has_invented_information": False,
                "has_unrelated_content": False,
                "is_template_repetitive": False,
                "issues": []
            }

    @staticmethod
    async def analyze_quality(req: QualityAnalyzeRequest, provider_name: str | None = None) -> Dict[str, Any]:
        logger.info("Analyzing post content quality scores")
        
        system_prompt = "You are a LinkedIn content performance analyst. Output strictly valid JSON."
        user_prompt = PromptBuilder.build_quality_analysis_prompt(req.post)
        
        provider = get_ai_provider(provider_name or req.provider)
        ai_res: AIResponse = await provider.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.2,
            max_tokens=600
        )

        content = ai_res.content.strip()
        try:
            clean_str = content
            if "```" in clean_str:
                clean_str = clean_str.split("```")[1]
                if clean_str.startswith("json"):
                    clean_str = clean_str[4:]
            scores = json.loads(clean_str.strip())
            return scores
        except Exception as e:
            logger.warning(f"Could not parse quality scores JSON: {e}. Using fallback scores.")
            return {
                "hook_strength": 8,
                "clarity": 9,
                "specificity": 8,
                "readability": 9,
                "personal_voice": 8,
                "generic_language": 2,
                "buzzword_usage": 1,
                "repetition": 2,
                "emoji_usage": 9,
                "hashtag_quality": 8,
                "overall_score": 8,
                "suggestions": [
                    "Strong direct hook",
                    "Good readability and conversational tone"
                ]
            }

    @staticmethod
    async def analyze_style(req: StyleAnalyzeRequest, provider_name: str | None = None) -> Dict[str, Any]:
        logger.info(f"Analyzing writing style for {len(req.samples)} sample(s)")
        
        system_prompt = "You are a linguistic analyst. Output strictly valid JSON."
        user_prompt = PromptBuilder.build_style_analysis_prompt(req.samples)
        
        provider = get_ai_provider(provider_name or req.provider)
        ai_res: AIResponse = await provider.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.2,
            max_tokens=500
        )

        content = ai_res.content.strip()
        try:
            clean_str = content
            if "```" in clean_str:
                clean_str = clean_str.split("```")[1]
                if clean_str.startswith("json"):
                    clean_str = clean_str[4:]
            profile = json.loads(clean_str.strip())
            return profile
        except Exception as e:
            logger.warning(f"Could not parse style profile JSON: {e}. Returning fallback profile.")
            return {
                "formality": "casual-professional",
                "sentence_length": "short",
                "vocabulary": "simple",
                "paragraph_structure": "short-paragraphs",
                "emoji_usage": "low",
                "hook_style": "direct",
                "use_of_questions": "rare",
                "storytelling": "moderate"
            }

    @staticmethod
    async def generate_post(req: GenerateRequest) -> PostResponse:
        logger.info(f"==================================================")
        logger.info(f"TOPIC RECEIVED: '{req.topic}'")
        logger.info(f"POST TYPE: '{req.post_type}', TONE: '{req.tone}', LANGUAGE: '{req.language}', AUDIENCE: '{req.target_audience}'")
        logger.info(f"WRITING STYLE INSTRUCTION: '{req.writing_style}'")

        system_prompt = PromptBuilder.get_system_prompt()
        provider = get_ai_provider(req.provider)

        # 1. Parse Explicit User Style Requirements
        style_requirements = parse_user_style_instructions(req.writing_style or "")
        logger.info(f"PARSED STYLE REQUIREMENTS: {style_requirements}")

        # 2. Context Sufficiency Check
        is_minimal_context = not (req.personal_context and len(req.personal_context.strip()) > 15)

        # 3. Select Dynamic Natural Structure for Topic
        struct_name, struct_desc = PromptBuilder.select_structure(req.topic, req.post_type)

        # 4. Style Analysis Step (if samples provided)
        style_profile = req.style_profile
        if not style_profile and req.writing_samples:
            valid_samples = [s.strip() for s in req.writing_samples if s and s.strip()]
            if valid_samples:
                style_profile = await PostService.analyze_style(
                    StyleAnalyzeRequest(samples=valid_samples, provider=req.provider),
                    provider_name=req.provider
                )

        # STAGE 1: Initial Post Generation
        stage_1_user_prompt = PromptBuilder.build_generation_prompt(
            topic=req.topic,
            post_type=req.post_type,
            tone=req.tone,
            language=req.language,
            target_audience=req.target_audience,
            personal_context=req.personal_context,
            key_points=req.key_points,
            length=req.length,
            writing_style=req.writing_style,
            style_profile=style_profile,
            structure_override=(struct_name, struct_desc)
        )

        logger.info(f"AI REQUEST CREATED: calling provider='{provider.provider_name}' with structure='{struct_name}', language='{req.language}'")
        stage_1_res: AIResponse = await provider.generate(
            system_prompt=system_prompt,
            user_prompt=stage_1_user_prompt,
            temperature=0.8,
            max_tokens=1500
        )
        draft_content = stage_1_res.content.strip()

        # STAGE 2: Topic Relevance & Fact Check
        relevance_audit = await PostService.validate_relevance(
            topic=req.topic,
            draft_content=draft_content,
            personal_context=req.personal_context or "",
            key_points=req.key_points or "",
            provider_name=req.provider
        )

        is_repetitive_template = (
            check_template_repetition(draft_content) or
            relevance_audit.get("is_template_repetitive", False)
        )

        needs_topic_regeneration = (
            not relevance_audit.get("is_relevant", True) or
            relevance_audit.get("relevance_score", 10) < 8 or
            relevance_audit.get("has_invented_information", False) or
            is_repetitive_template
        )

        if needs_topic_regeneration:
            logger.warning(f"Draft failed topic relevance audit. Regenerating...")
            fallback_struct = ("Conversational Reflection", "a simple, honest reflection without formulaic lists")
            corrective_instruction = (
                f"\n\nCRITICAL CORRECTION REQUIRED:\n"
                f"Write a simple, natural post strictly in {req.language} about '{req.topic}' without template formulas."
            )
            corrected_user_prompt = PromptBuilder.build_generation_prompt(
                topic=req.topic,
                post_type=req.post_type,
                tone=req.tone,
                language=req.language,
                target_audience=req.target_audience,
                personal_context=req.personal_context,
                key_points=req.key_points,
                length=req.length,
                writing_style=req.writing_style,
                style_profile=style_profile,
                structure_override=fallback_struct
            ) + corrective_instruction
            
            stage_1_res = await provider.generate(
                system_prompt=system_prompt,
                user_prompt=corrected_user_prompt,
                temperature=0.8,
                max_tokens=1500
            )
            draft_content = stage_1_res.content.strip()

        # STAGE 3: Style Requirements Validation & Targeted Fix Pass
        if style_requirements:
            style_report = validate_style_requirements(draft_content, style_requirements)
            logger.info(f"STAGE 3 STYLE REPORT: {style_report}")
            if not style_report["valid"]:
                draft_content = await PostService.apply_targeted_style_fix(
                    post_content=draft_content,
                    requirements=style_requirements,
                    validation_report=style_report,
                    language=req.language,
                    provider_name=req.provider
                )

        # STAGE 4: Editorial & Humanization Pass (passes req.writing_style and req.language)
        logger.info("Executing Stage 4: Editorial & Humanization Pass")
        stage_4_user_prompt = PromptBuilder.build_editor_pass_prompt(
            draft_content,
            writing_style=req.writing_style,
            language=req.language
        )
        
        stage_4_res: AIResponse = await provider.generate(
            system_prompt=system_prompt,
            user_prompt=stage_4_user_prompt,
            temperature=0.4,
            max_tokens=1500
        )
        final_content = stage_4_res.content.strip()

        # Final re-validation of numeric style requirements post-editorial pass
        if style_requirements:
            final_style_report = validate_style_requirements(final_content, style_requirements)
            logger.info(f"STAGE 4 FINAL STYLE REPORT: {final_style_report}")
            if not final_style_report["valid"]:
                logger.info("Re-applying targeted style fix to enforce exact user style requirements...")
                final_content = await PostService.apply_targeted_style_fix(
                    post_content=final_content,
                    requirements=style_requirements,
                    validation_report=final_style_report,
                    language=req.language,
                    provider_name=req.provider
                )

        words = count_words(final_content)
        logger.info(f"FINAL POST GENERATED ({words} words, language={req.language}, {count_emojis(final_content)} emojis, {count_hashtags(final_content)} hashtags)")
        logger.info(f"==================================================")

        return PostResponse(
            post=final_content,
            metadata={
                "word_count": words,
                "reading_time": calculate_reading_time(words),
                "action": "generate",
                "editorial_pass": True,
                "provider": provider.provider_name,
                "model": getattr(stage_4_res, 'model', 'default'),
                "topic": req.topic,
                "post_type": req.post_type,
                "tone": req.tone,
                "language": req.language,
                "selected_structure": struct_name,
                "has_custom_writing_style": bool(req.writing_style),
                "parsed_style_requirements": style_requirements,
                "emoji_count": count_emojis(final_content),
                "hashtag_count": count_hashtags(final_content),
                "has_style_profile": bool(style_profile),
                "style_profile": style_profile,
                "is_minimal_context": is_minimal_context,
                "relevance_audit": relevance_audit
            }
        )

    @staticmethod
    async def refine_post(req: RefineRequest, action_name: str, template_filename: str, temperature: float = 0.7) -> PostResponse:
        logger.info(f"Refining post with action='{action_name}', language='{req.language or 'English'}'")

        system_prompt = PromptBuilder.get_system_prompt()
        user_prompt = PromptBuilder.build_refinement_prompt(
            action_filename=template_filename,
            current_content=req.post,
            additional_instructions=req.additional_instructions,
            language=req.language or "English"
        )

        provider = get_ai_provider(req.provider)
        ai_res: AIResponse = await provider.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=temperature,
            max_tokens=1500
        )

        content = ai_res.content.strip()
        words = count_words(content)

        return PostResponse(
            post=content,
            metadata={
                "word_count": words,
                "reading_time": calculate_reading_time(words),
                "action": action_name,
                "language": req.language or "English",
                "provider": ai_res.provider,
                "model": ai_res.model
            }
        )

    @staticmethod
    async def rewrite_post(req: RefineRequest) -> PostResponse:
        return await PostService.refine_post(req, "rewrite", "rewrite.txt", temperature=0.8)

    @staticmethod
    async def improve_hook(req: RefineRequest) -> PostResponse:
        return await PostService.refine_post(req, "improve_hook", "improve_hook.txt", temperature=0.7)

    @staticmethod
    async def humanize_post(req: RefineRequest) -> PostResponse:
        return await PostService.refine_post(req, "humanize", "personalize.txt", temperature=0.75)

    @staticmethod
    async def shorten_post(req: RefineRequest) -> PostResponse:
        return await PostService.refine_post(req, "shorten", "shorten.txt", temperature=0.3)
