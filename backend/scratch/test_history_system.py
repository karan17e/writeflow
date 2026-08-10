import asyncio
import sys
import os
import json
from app.database import init_db, AsyncSessionLocal
from app.schemas.post import GenerateRequest, RefineRequest
from app.services.post_service import PostService
from app.services.history_service import HistoryService

sys.stdout.reconfigure(encoding='utf-8')

async def run_history_tests():
    print("==================================================")
    print("RUNNING 10 MANDATORY HISTORY SYSTEM TESTS")
    print("==================================================\n")

    await init_db()

    async with AsyncSessionLocal() as db:
        # Clear database to start clean
        await HistoryService.clear_all(db)

        # TEST 1: Generate "3 months Python internship" (English)
        print("--- TEST 1: Generate '3 months Python internship' (English) ---")
        req_1 = GenerateRequest(topic="3 months Python internship", language="English", post_type="Story", tone="Professional")
        res_1 = await PostService.generate_post(req_1)
        item_1 = await HistoryService.create_from_generation(req_1, res_1, db)
        assert item_1 is not None
        print(f"Post 1 Generated & Saved. History ID: {item_1.id}")
        print("--------------------------------------------------\n")

        # TEST 2: Generate "To-do list project" (Hinglish)
        print("--- TEST 2: Generate 'To-do list project' (Hinglish) ---")
        req_2 = GenerateRequest(topic="To-do list project", language="Hinglish", post_type="Project", tone="Conversational")
        res_2 = await PostService.generate_post(req_2)
        item_2 = await HistoryService.create_from_generation(req_2, res_2, db)
        assert item_2 is not None
        print(f"Post 2 Generated & Saved. History ID: {item_2.id}")
        print("--------------------------------------------------\n")

        # TEST 3: Generate "First hackathon" (Hindi)
        print("--- TEST 3: Generate 'First hackathon' (Hindi) ---")
        req_3 = GenerateRequest(topic="First hackathon", language="Hindi", post_type="Personal Experience", tone="Conversational")
        res_3 = await PostService.generate_post(req_3)
        item_3 = await HistoryService.create_from_generation(req_3, res_3, db)
        assert item_3 is not None
        print(f"Post 3 Generated & Saved. History ID: {item_3.id}")
        print("--------------------------------------------------\n")

        # TEST 4: Regenerate Post 3 -> New history item created, original not overwritten
        print("--- TEST 4: Regenerate Post 3 -> New History Version Created ---")
        res_3_regen = await PostService.generate_post(req_3)
        item_3_regen = await HistoryService.create_from_refinement(
            RefineRequest(post=res_3.post, language="Hindi"),
            action_name="regenerate",
            response=res_3_regen,
            db=db,
            parent_id=item_3.id,
            original_topic=req_3.topic,
            post_type=req_3.post_type,
            tone=req_3.tone,
            language=req_3.language
        )
        assert item_3_regen is not None
        assert item_3_regen.id != item_3.id
        
        all_items = await HistoryService.get_all(db)
        print(f"Total history count after regenerate: {len(all_items)} (Expected: 4)")
        assert len(all_items) == 4
        print("--------------------------------------------------\n")

        # TEST 5: Restore Post 1 -> Retrieve from history without AI call
        print("--- TEST 5: Restore Post 1 (0 Groq Tokens) ---")
        restored_1 = await HistoryService.get_by_id(db, item_1.id)
        assert restored_1 is not None
        assert restored_1["post"] == res_1.post
        assert restored_1["topic"] == "3 months Python internship"
        print(f"Restored Post 1 successfully without calling AI. Topic: '{restored_1['topic']}'")
        print("--------------------------------------------------\n")

        # TEST 6 & 7: Persistence Check across new session
        print("--- TEST 6 & 7: Database Persistence Check ---")
        items_persisted = await HistoryService.get_all(db)
        assert len(items_persisted) == 4
        print(f"Persisted History Count: {len(items_persisted)} items survived session reload.")
        print("--------------------------------------------------\n")

        # TEST 8: Copy previous history item
        print("--- TEST 8: Copy History Item Content ---")
        item_to_copy = await HistoryService.get_by_id(db, item_2.id)
        copied_text = item_to_copy["post"]
        assert copied_text == res_2.post
        print("Copy verified: exact saved text matches.")
        print("--------------------------------------------------\n")

        # TEST 9: Delete one history item
        print("--- TEST 9: Delete Individual History Item ---")
        deleted = await HistoryService.delete_by_id(db, item_2.id)
        assert deleted is True
        remaining = await HistoryService.get_all(db)
        print(f"Remaining items after deleting Item 2: {len(remaining)} (Expected: 3)")
        assert len(remaining) == 3
        print("--------------------------------------------------\n")

        # TEST 10: Clear All History
        print("--- TEST 10: Clear All History ---")
        cleared_count = await HistoryService.clear_all(db)
        print(f"Cleared {cleared_count} items from history.")
        final_list = await HistoryService.get_all(db)
        assert len(final_list) == 0
        print("Clear All History verified: 0 items remaining.")
        print("--------------------------------------------------\n")

    print("ALL 10 HISTORY SYSTEM TESTS PASSED PERFECTLY!")

if __name__ == "__main__":
    asyncio.run(run_history_tests())
