import urllib.request
import json

BASE_URL = "http://localhost:8000/api"

def make_request(url, method="GET", data=None):
    headers = {"Content-Type": "application/json"}
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req) as resp:
        content = resp.read().decode("utf-8")
        return resp.status, json.loads(content) if content else None

def run_test():
    print("==================================================")
    print("TESTING LIVE FASTAPI BACKEND API AT http://localhost:8000")
    print("==================================================\n")

    # 1. Health Check
    status, res = make_request(f"{BASE_URL}/health")
    print(f"1. Health Check: Status {status}, Response: {res}")

    # 2. Get History (Initial)
    status, history = make_request(f"{BASE_URL}/history")
    print(f"2. Get History (Initial): Status {status}, Count: {len(history)}")

    # 3. Generate Post 1
    gen_payload_1 = {
        "topic": "Live API History Integration Test",
        "post_type": "Story",
        "tone": "Conversational",
        "language": "English",
        "length": "Short"
    }
    status, post_1 = make_request(f"{BASE_URL}/generate", method="POST", data=gen_payload_1)
    print(f"3. Generate Post 1: Status {status}, Post snippet: '{post_1['post'][:60]}...'")

    # 4. Get History after Generate
    status, history_after_1 = make_request(f"{BASE_URL}/history")
    print(f"4. Get History after Generate: Status {status}, Count: {len(history_after_1)} (Expected >= 1)")
    assert len(history_after_1) >= 1
    first_item = history_after_1[0]
    print(f"   Saved History Item ID: '{first_item['id']}', Topic: '{first_item['topic']}'")

    # 5. Delete History Item
    status, del_res = make_request(f"{BASE_URL}/history/{first_item['id']}", method="DELETE")
    print(f"5. Delete History Item: Status {status}, Response: {del_res}")

    print("\nALL LIVE API INTEGRATION TESTS COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    run_test()
