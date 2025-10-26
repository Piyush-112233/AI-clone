from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from groq import Groq
import auth

# Load environment variables
load_dotenv()

app = FastAPI(title="LinguaSpark AI", version="3.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Groq AI client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ============ REQUEST MODELS ============

class SignupRequest(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class Message(BaseModel):
    username: str
    text: str
    user_lang: str
    target_lang: str

class GrammarCheckRequest(BaseModel):
    username: str
    text: str
    language: str

class VocabularyRequest(BaseModel):
    username: str
    word: str
    language: str

# ============ AUTH ENDPOINTS ============

@app.post("/signup")
async def signup(request: SignupRequest):
    """Register new user"""
    result = auth.create_user(request.username, request.email, request.password)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@app.post("/login")
async def login(request: LoginRequest):
    """Login user"""
    result = auth.login_user(request.username, request.password)
    if not result["success"]:
        raise HTTPException(status_code=401, detail=result["message"])
    return result

@app.get("/history/{username}")
async def get_history(username: str):
    """Get user's chat history"""
    history = auth.get_chat_history(username)
    return {"history": history}

# ============ MAIN CHAT ENDPOINT ============

@app.post("/chat")
async def chat(message: Message):
    try:
        user = auth.get_user(message.username)
        if not user:
            return {"reply": "⚠️ Please login first"}
        
        prompt = f"""You are LinguaSpark, an expert language teacher AI. 

User's message: "{message.text}"
User's language: {message.user_lang}
Target language to learn: {message.target_lang}

Your task:
1. **Translate** the message to {message.target_lang}
2. **Check grammar** - if there are mistakes in the user's {message.user_lang}, gently correct them
3. **Explain** the translation in a friendly way
4. **Provide examples** (1-2 simple ones)
5. **Teach vocabulary** - highlight key words and their meanings
6. **Give pronunciation tips** if helpful
7. **Encourage** the learner

Format your response like this:
📝 Translation: [translation here]
✅ Grammar: [if mistakes, show correction, else say "Perfect!"]
💡 Explanation: [explain the translation]
📚 Key Vocabulary: [list 2-3 important words with meanings]
🗣️ Pronunciation: [tips if needed]

Keep it concise (3-4 paragraphs max) and engaging!"""

        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are LinguaSpark, a friendly and expert language teacher who corrects mistakes gently."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=600,
            temperature=0.7,
        )

        reply = response.choices[0].message.content
        
        # Save to history
        try:
            auth.save_chat_history(message.username, message.text, reply)
        except Exception as chat_error:
            print(f"Error saving chat history: {chat_error}")
        
        # 🆕 NEW: Update stats and award points
        try:
            auth.update_stats(message.username, 'message')
        except Exception as stats_error:
            print(f"Error updating stats: {stats_error}")
        
        return {"reply": reply}

    except Exception as e:
        print(f"Chat error: {str(e)}")
        return {"reply": f"❌ Error: Unable to process your message. Please try again."}

# ============ GRAMMAR CHECK ============

@app.post("/grammar-check")
async def grammar_check(request: GrammarCheckRequest):
    try:
        user = auth.get_user(request.username)
        if not user:
            return {"error": "Please login first"}
        
        prompt = f"""You are a {request.language} grammar expert.

Analyze this sentence: "{request.text}"

Provide:
1. **Corrections** - List all grammar mistakes
2. **Corrected Version** - Show the correct sentence
3. **Explanation** - Explain why it was wrong (in simple terms)
4. **Tips** - Give 1-2 tips to avoid this mistake

If the sentence is perfect, say so and praise the user!

Keep it short and encouraging."""

        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": f"You are a {request.language} grammar teacher."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.5,
        )

        # 🆕 NEW: Update stats
        try:
            auth.update_stats(request.username, 'grammar')
        except Exception as e:
            print(f"Error updating grammar stats: {e}")

        return {
            "original": request.text,
            "analysis": response.choices[0].message.content,
            "language": request.language
        }

    except Exception as e:
        return {"error": f"Error: {str(e)}"}

# ============ VOCABULARY ============

@app.post("/vocabulary")
async def vocabulary_explain(request: VocabularyRequest):
    try:
        user = auth.get_user(request.username)
        if not user:
            return {"error": "Please login first"}
        
        prompt = f"""You are a {request.language} vocabulary expert.

Explain the word: "{request.word}"

Provide:
1. **Meaning** - Simple definition
2. **Part of Speech** - (noun, verb, adjective, etc.)
3. **Example Sentences** - Give 3 simple examples
4. **Synonyms** - List 2-3 similar words
5. **Common Phrases** - Show 2 common phrases using this word
6. **Pronunciation** - How to pronounce it

Make it simple and easy to understand!"""

        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": f"You are a {request.language} vocabulary teacher."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.6,
        )

        # 🆕 NEW: Update stats
        try:
            auth.update_stats(request.username, 'vocab')
        except Exception as e:
            print(f"Error updating vocab stats: {e}")

        return {
            "word": request.word,
            "language": request.language,
            "explanation": response.choices[0].message.content
        }

    except Exception as e:
        return {"error": f"Error: {str(e)}"}

# ============ 🆕 NEW: PROGRESS TRACKING ENDPOINTS ============

@app.get("/progress/{username}")
async def get_progress(username: str):
    """
    Get user's progress dashboard data
    Shows stats, achievements, level, etc.
    """
    progress = auth.get_progress(username)
    if not progress:
        raise HTTPException(status_code=404, detail="User not found")
    return progress

@app.get("/weekly-insights/{username}")
async def get_weekly_insights(username: str):
    """
    Get AI-generated weekly insights
    Shows weekly summary and motivation
    """
    insights = auth.get_weekly_insights(username)
    if not insights:
        raise HTTPException(status_code=404, detail="User not found")
    return insights

@app.get("/achievements/{username}")
async def get_achievements(username: str):
    """
    Get user's earned achievements
    """
    user = auth.get_user(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    achievements = auth.get_user_achievements(username)
    
    return {
        "username": username,
        "achievements": achievements,
        "total": len(achievements)
    }

@app.get("/stats/{username}")
async def get_user_stats(username: str):
    """
    Get user's statistics only
    Lightweight endpoint for quick stat checks
    """
    user = auth.get_user(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    stats = auth.get_user_stats_only(username)
    
    if not stats:
        raise HTTPException(status_code=404, detail="Stats not found")
    
    return {
        "username": username,
        "stats": stats
    }

@app.get("/leaderboard")
async def get_leaderboard(limit: int = 10):
    """
    Get top users by points
    Returns leaderboard with rankings
    """
    try:
        from supabase import create_client
        import os
        supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
        
        # Get users with their stats, ordered by points
        query = """
            SELECT 
                u.username,
                u.email,
                s.total_points,
                s.level,
                s.total_messages,
                s.current_streak,
                s.words_learned
            FROM users u
            JOIN user_stats s ON u.id = s.user_id
            ORDER BY s.total_points DESC
            LIMIT {}
        """.format(limit)
        
        # Alternative: Use table queries
        stats_response = supabase.table('user_stats').select('*, users(username, email)').order('total_points', desc=True).limit(limit).execute()
        
        leaderboard = []
        for idx, stat in enumerate(stats_response.data if stats_response.data else [], 1):
            leaderboard.append({
                "rank": idx,
                "username": stat.get('users', {}).get('username', 'Unknown'),
                "level": stat.get('level', 1),
                "total_points": stat.get('total_points', 0),
                "total_messages": stat.get('total_messages', 0),
                "current_streak": stat.get('current_streak', 0),
                "words_learned": stat.get('words_learned', 0)
            })
        
        return {
            "leaderboard": leaderboard,
            "total": len(leaderboard)
        }
    except Exception as e:
        print(f"Error getting leaderboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============ ROOT & HEALTH ============

@app.get("/")
async def root():
    return {
        "message": "🌟 LinguaSpark AI v3.0 - Gamified Learning!",
        "version": "3.0.0",
        "status": "active",
        "database": "Supabase PostgreSQL",
        "endpoints": {
            "auth": {
                "POST /signup": "Register new user",
                "POST /login": "Login user"
            },
            "learning": {
                "POST /chat": "Smart language learning chat",
                "POST /grammar-check": "Grammar correction",
                "POST /vocabulary": "Word explanations"
            },
            "progress": {
                "GET /progress/{username}": "User progress dashboard",
                "GET /stats/{username}": "User statistics only",
                "GET /achievements/{username}": "User achievements",
                "GET /weekly-insights/{username}": "Weekly AI insights",
                "GET /history/{username}": "Chat history"
            },
            "community": {
                "GET /leaderboard": "Top users by points"
            }
        },
        "features": [
            "✅ Smart language learning chat",
            "✅ Grammar correction with AI",
            "✅ Vocabulary explanations",
            "✅ Progress tracking & stats",
            "✅ Gamified achievements system",
            "✅ Daily streak tracking",
            "✅ Weekly AI insights",
            "✅ User leaderboard",
            "✅ Supabase database integration"
        ]
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "3.0.0"}