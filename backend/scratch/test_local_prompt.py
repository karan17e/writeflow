import asyncio
import sys
from app.schemas.post import GenerateRequest, RefineRequest
from app.services.post_service import PostService
from app.prompts.prompt_builder import PromptBuilder

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    print("=== TEST 1: Hindi Generation ===")
    req_hi = GenerateRequest(
        topic="3 months Python internship",
        language="Hindi",
        tone="Professional",
        target_audience="Recruiters",
        writing_style="Use 3 emojis and simple language."
    )
    res_hi = await PostService.generate_post(req_hi)
    print("HINDI OUTPUT:\n", res_hi.post)
    print("\nMetadata:", res_hi.metadata)

    print("\n=== TEST 2: Hinglish Generation ===")
    req_hing = GenerateRequest(
        topic="3 months Python internship",
        language="Hinglish",
        tone="Professional",
        target_audience="Recruiters",
        writing_style="Use 3 emojis and simple language."
    )
    res_hing = await PostService.generate_post(req_hing)
    print("HINGLISH OUTPUT:\n", res_hing.post)
    print("\nMetadata:", res_hing.metadata)

if __name__ == "__main__":
    asyncio.run(main())
