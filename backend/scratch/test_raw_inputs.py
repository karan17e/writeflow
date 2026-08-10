import asyncio
import sys
import re
from app.schemas.post import GenerateRequest
from app.services.post_service import PostService

sys.stdout.reconfigure(encoding='utf-8')

def contains_devanagari(text: str) -> bool:
    return bool(re.search(r'[\u0900-\u097F]', text))

async def run_raw_input_tests():
    print("==================================================")
    print("RUNNING RAW TOPIC INTERPRETATION TESTS (GROQ API)")
    print("==================================================\n")

    # TEST 1
    print("--- TEST 1: 'meh ek to do ist project banaya hai' -> English ---")
    topic_1 = "meh ek to do ist project banaya hai"
    req_1 = GenerateRequest(topic=topic_1, language="English", post_type="Project", tone="Conversational")
    res_1 = await PostService.generate_post(req_1)
    post_1 = res_1.post
    print("OUTPUT:\n", post_1)
    is_copied_1 = bool(re.search(r'\bmeh\b', post_1, re.I)) or bool(re.search(r'\bist\b', post_1, re.I)) or topic_1.lower() in post_1.lower()
    print(f"VERIFICATION: Raw input quoted/copied? {is_copied_1} (Target: False)")
    print("--------------------------------------------------\n")

    # TEST 2
    print("--- TEST 2: '3 month python intern complete' -> Hinglish ---")
    topic_2 = "3 month python intern complete"
    req_2 = GenerateRequest(topic=topic_2, language="Hinglish", post_type="Story", tone="Conversational")
    res_2 = await PostService.generate_post(req_2)
    post_2 = res_2.post
    print("OUTPUT:\n", post_2)
    is_copied_2 = topic_2.lower() in post_2.lower()
    print(f"VERIFICATION: Raw input quoted/copied? {is_copied_2} (Target: False), Is Roman Hinglish? {not contains_devanagari(post_2)}")
    print("--------------------------------------------------\n")

    # TEST 3
    print("--- TEST 3: 'first hackathon me participate kiya' -> Hindi ---")
    topic_3 = "first hackathon me participate kiya"
    req_3 = GenerateRequest(topic=topic_3, language="Hindi", post_type="Personal Experience", tone="Conversational")
    res_3 = await PostService.generate_post(req_3)
    post_3 = res_3.post
    print("OUTPUT:\n", post_3)
    print(f"VERIFICATION: Is Devanagari Hindi? {contains_devanagari(post_3)}")
    print("--------------------------------------------------\n")

    # TEST 4
    print("--- TEST 4: 'college me ai project bnaya' -> English ---")
    topic_4 = "college me ai project bnaya"
    req_4 = GenerateRequest(topic=topic_4, language="English", post_type="Project", tone="Conversational")
    res_4 = await PostService.generate_post(req_4)
    post_4 = res_4.post
    print("OUTPUT:\n", post_4)
    is_copied_4 = "bnaya" in post_4.lower() or "college me ai project" in post_4.lower()
    print(f"VERIFICATION: Raw input quoted/copied? {is_copied_4} (Target: False)")
    print("--------------------------------------------------\n")

if __name__ == "__main__":
    asyncio.run(run_raw_input_tests())
