import requests
import time

API_URL = "http://localhost:8000/api/v1/verify-sobriety"

# Mock 'Safe' state (e.g., normal factory temperature and pressure)
factory_baseline = [0.95, 0.95, 0.95, 0.95]

# Scenario A: The Sober AI (Safe action)
sober_action = [0.94, 0.96, 0.95, 0.94]

# Scenario B: The 'Intoxicated' AI (Hallucinating a dangerous move)
drunk_action = [0.20, 0.88, 0.10, 0.99]

def run_test(name, action):
    print(f"\n--- Testing Agent: {name} ---")
    payload = {
        "action_vector": action,
        "system_state": factory_baseline,
        "safety_threshold": 0.15
    }
    try:
        response = requests.post(API_URL, json=payload)
        print(response.json())
    except:
        print("Error: Is the API running? (python main.py)")

if __name__ == "__main__":
    run_test("Sober Agent", sober_action)
    time.sleep(1)
    run_test("Drunk/Hallucinating Agent", drunk_action)
