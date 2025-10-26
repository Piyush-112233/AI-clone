import uvicorn
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    print("🌟 Starting LinguaSpark AI Server...")
    print(f"Server running at: http://127.0.0.1:8000")
    print(f"API Documentation: http://127.0.0.1:8000/docs")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)