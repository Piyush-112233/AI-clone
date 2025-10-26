"""
Test Script for LinguaSpark AI API
Tests all endpoints with Supabase integration
"""

import requests
import json

API_URL = "http://localhost:8000"
test_user = {
    "username": "testuser_" + str(int(__import__('time').time())),
    "email": f"test_{int(__import__('time').time())}@example.com",
    "password": "test123456"
}

def print_result(title, response):
    print(f"\n{'='*60}")
    print(f"🧪 {title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")
    print(f"{'='*60}\n")

def main():
    print("\n" + "="*60)
    print("🚀 LINGUASPARK AI - SUPABASE INTEGRATION TEST")
    print("="*60 + "\n")
    
    # 1. Test Root
    print("1️⃣ Testing Root Endpoint...")
    response = requests.get(f"{API_URL}/")
    print_result("GET /", response)
    
    # 2. Test Health
    print("2️⃣ Testing Health Check...")
    response = requests.get(f"{API_URL}/health")
    print_result("GET /health", response)
    
    # 3. Test Signup
    print("3️⃣ Testing Signup...")
    response = requests.post(f"{API_URL}/signup", json=test_user)
    print_result("POST /signup", response)
    
    if response.status_code != 200:
        print("❌ Signup failed! Stopping tests.")
        return
    
    # 4. Test Login
    print("4️⃣ Testing Login...")
    response = requests.post(f"{API_URL}/login", json={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    print_result("POST /login", response)
    
    if response.status_code != 200:
        print("❌ Login failed! Stopping tests.")
        return
    
    username = test_user["username"]
    
    # 5. Test Chat
    print("5️⃣ Testing Chat...")
    response = requests.post(f"{API_URL}/chat", json={
        "username": username,
        "text": "Hello, how are you?",
        "user_lang": "English",
        "target_lang": "Spanish"
    })
    print_result("POST /chat", response)
    
    # 6. Test Grammar Check
    print("6️⃣ Testing Grammar Check...")
    response = requests.post(f"{API_URL}/grammar-check", json={
        "username": username,
        "text": "I goes to school yesterday",
        "language": "English"
    })
    print_result("POST /grammar-check", response)
    
    # 7. Test Vocabulary
    print("7️⃣ Testing Vocabulary...")
    response = requests.post(f"{API_URL}/vocabulary", json={
        "username": username,
        "word": "Hello",
        "language": "Spanish"
    })
    print_result("POST /vocabulary", response)
    
    # 8. Test Stats
    print("8️⃣ Testing Stats...")
    response = requests.get(f"{API_URL}/stats/{username}")
    print_result(f"GET /stats/{username}", response)
    
    # 9. Test Progress
    print("9️⃣ Testing Progress...")
    response = requests.get(f"{API_URL}/progress/{username}")
    print_result(f"GET /progress/{username}", response)
    
    # 10. Test Achievements
    print("🔟 Testing Achievements...")
    response = requests.get(f"{API_URL}/achievements/{username}")
    print_result(f"GET /achievements/{username}", response)
    
    # 11. Test History
    print("1️⃣1️⃣ Testing History...")
    response = requests.get(f"{API_URL}/history/{username}")
    print_result(f"GET /history/{username}", response)
    
    # 12. Test Weekly Insights
    print("1️⃣2️⃣ Testing Weekly Insights...")
    response = requests.get(f"{API_URL}/weekly-insights/{username}")
    print_result(f"GET /weekly-insights/{username}", response)
    
    # 13. Test Leaderboard
    print("1️⃣3️⃣ Testing Leaderboard...")
    response = requests.get(f"{API_URL}/leaderboard")
    print_result("GET /leaderboard", response)
    
    print("\n" + "="*60)
    print("✅ ALL TESTS COMPLETED!")
    print("="*60)
    print(f"\n📝 Test User Created: {username}")
    print(f"📧 Email: {test_user['email']}")
    print("\n💡 Check your Supabase database to verify data storage!")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to API!")
        print("Make sure the server is running:")
        print("  cd backend")
        print("  uvicorn main:app --reload")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
