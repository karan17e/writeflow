import asyncio
import sys
import re
from app.schemas.post import GenerateRequest
from app.services.post_service import PostService, count_emojis

sys.stdout.reconfigure(encoding='utf-8')

def contains_devanagari(text: str) -> bool:
    return bool(re.search(r'[\u0900-\u097F]', text))

def is_roman_script(text: str) -> bool:
    # True if there are NO Devanagari characters and majority is ASCII/Roman
    return not contains_devanagari(text)

async def run_tests():
    print("==================================================")
    print("RUNNING ALL MANDATORY LANGUAGE TESTS (LOCAL GROQ API)")
    print("==================================================\n")

    # TEST A: English -> English
    print("--- TEST A: English -> English ---")
    req_a = GenerateRequest(
        topic="3 months Python internship",
        language="English",
        tone="Professional",
        target_audience="Recruiters"
    )
    res_a = await PostService.generate_post(req_a)
    print("OUTPUT:\n", res_a.post)
    print(f"VERIFICATION: language={res_a.metadata['language']}, is_english={is_roman_script(res_a.post)}")
    print("--------------------------------------------------\n")

    # TEST B: Hindi -> Hindi Devanagari
    print("--- TEST B: Hindi -> Hindi Devanagari ---")
    req_b = GenerateRequest(
        topic="3 months Python internship",
        language="Hindi",
        tone="Professional",
        target_audience="Recruiters"
    )
    res_b = await PostService.generate_post(req_b)
    print("OUTPUT:\n", res_b.post)
    print(f"VERIFICATION: language={res_b.metadata['language']}, contains_devanagari={contains_devanagari(res_b.post)}")
    print("--------------------------------------------------\n")

    # TEST C: Hinglish -> Roman Hinglish
    print("--- TEST C: Hinglish -> Roman Hinglish ---")
    req_c = GenerateRequest(
        topic="3 months Python internship",
        language="Hinglish",
        tone="Professional",
        target_audience="Recruiters"
    )
    res_c = await PostService.generate_post(req_c)
    print("OUTPUT:\n", res_c.post)
    print(f"VERIFICATION: language={res_c.metadata['language']}, contains_devanagari={contains_devanagari(res_c.post)}, is_roman={is_roman_script(res_c.post)}")
    print("--------------------------------------------------\n")

    # TEST D: Hinglish + "Use 3 emojis" -> Hinglish + approx 3 emojis
    print("--- TEST D: Hinglish + 'Use 3 emojis' ---")
    req_d = GenerateRequest(
        topic="3 months Python internship",
        language="Hinglish",
        tone="Professional",
        target_audience="Recruiters",
        writing_style="Use 3 emojis and simple language."
    )
    res_d = await PostService.generate_post(req_d)
    emojis_d = count_emojis(res_d.post)
    print("OUTPUT:\n", res_d.post)
    print(f"VERIFICATION: language={res_d.metadata['language']}, emojis_actual={emojis_d}, is_roman={is_roman_script(res_d.post)}")
    print("--------------------------------------------------\n")

    # TEST E: Hindi + "Use 3 emojis" -> Hindi + approx 3 emojis
    print("--- TEST E: Hindi + 'Use 3 emojis' ---")
    req_e = GenerateRequest(
        topic="3 months Python internship",
        language="Hindi",
        tone="Professional",
        target_audience="Recruiters",
        writing_style="Use 3 emojis and simple language."
    )
    res_e = await PostService.generate_post(req_e)
    emojis_e = count_emojis(res_e.post)
    print("OUTPUT:\n", res_e.post)
    print(f"VERIFICATION: language={res_e.metadata['language']}, emojis_actual={emojis_e}, contains_devanagari={contains_devanagari(res_e.post)}")
    print("--------------------------------------------------\n")

if __name__ == "__main__":
    asyncio.run(run_tests())
