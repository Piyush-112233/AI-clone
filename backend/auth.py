import hashlib
import os
from datetime import datetime, timedelta
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("⚠️ SUPABASE_URL and SUPABASE_KEY must be set in .env file")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def hash_password(password):
    """Hash password with SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def get_user_by_username(username):
    """Get user from Supabase by username"""
    try:
        response = supabase.table('users').select('*').eq('username', username).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error getting user: {e}")
        return None

def get_user_by_email(email):
    """Get user from Supabase by email"""
    try:
        response = supabase.table('users').select('*').eq('email', email).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error getting user by email: {e}")
        return None

def create_user(username, email, password):
    """Create a new user in Supabase"""
    try:
        # Check if user already exists
        if get_user_by_username(username):
            return {"success": False, "message": "Username already exists"}
        
        # Check if email already exists
        if get_user_by_email(email):
            return {"success": False, "message": "Email already exists"}
        
        # Create new user
        user_data = {
            "username": username,
            "email": email,
            "password": hash_password(password),
            "created_at": datetime.now().isoformat(),
        }
        
        response = supabase.table('users').insert(user_data).execute()
        
        if response.data:
            # Initialize user stats
            user_id = response.data[0]['id']
            stats_data = {
                "user_id": user_id,
                "total_messages": 0,
                "words_learned": 0,
                "grammar_checks": 0,
                "vocab_lookups": 0,
                "current_streak": 0,
                "longest_streak": 0,
                "last_activity": None,
                "total_points": 0,
                "level": 1,
            }
            supabase.table('user_stats').insert(stats_data).execute()
            
            return {"success": True, "message": "Account created successfully!"}
        else:
            return {"success": False, "message": "Failed to create account"}
            
    except Exception as e:
        print(f"Error creating user: {e}")
        return {"success": False, "message": f"Error: {str(e)}"}

def login_user(username, password):
    """Login user"""
    try:
        user = get_user_by_username(username)
        
        if not user:
            return {"success": False, "message": "Username not found"}
        
        if user['password'] != hash_password(password):
            return {"success": False, "message": "Incorrect password"}
        
        # Update last activity
        supabase.table('user_stats').update({
            "last_activity": datetime.now().isoformat()
        }).eq('user_id', user['id']).execute()
        
        # Get user stats
        stats_response = supabase.table('user_stats').select('*').eq('user_id', user['id']).execute()
        stats = stats_response.data[0] if stats_response.data else {}
        
        return {
            "success": True, 
            "message": "Login successful!",
            "user": {
                "username": username,
                "email": user['email'],
                "stats": stats
            }
        }
    except Exception as e:
        print(f"Login error: {e}")
        return {"success": False, "message": f"Login failed: {str(e)}"}

def get_user(username):
    """Get user data"""
    return get_user_by_username(username)

def save_chat_history(username, message, reply):
    """Save chat to user history"""
    try:
        user = get_user_by_username(username)
        if user:
            chat_data = {
                "user_id": user['id'],
                "message": message,
                "reply": reply,
                "timestamp": datetime.now().isoformat()
            }
            supabase.table('chat_history').insert(chat_data).execute()
    except Exception as e:
        print(f"Error saving chat history: {e}")

def get_chat_history(username):
    """Get user's chat history"""
    try:
        user = get_user_by_username(username)
        if user:
            response = supabase.table('chat_history').select('*').eq('user_id', user['id']).order('timestamp', desc=True).limit(50).execute()
            return response.data if response.data else []
        return []
    except Exception as e:
        print(f"Error getting chat history: {e}")
        return []

# ============ 🆕 NEW: PROGRESS TRACKING FUNCTIONS ============

def update_stats(username, action_type, points=0):
    """
    Update user statistics based on actions
    action_type: 'message', 'grammar', 'vocab', 'achievement'
    """
    try:
        user = get_user_by_username(username)
        if not user:
            print(f"Warning: User {username} not found in update_stats")
            return False
        
        # Get current stats
        stats_response = supabase.table('user_stats').select('*').eq('user_id', user['id']).execute()
        if not stats_response.data:
            return False
        
        stats = stats_response.data[0]
        
        # Update based on action type
        updates = {}
        if action_type == 'message':
            updates['total_messages'] = stats['total_messages'] + 1
            updates['total_points'] = stats['total_points'] + 10
        elif action_type == 'grammar':
            updates['grammar_checks'] = stats['grammar_checks'] + 1
            updates['total_points'] = stats['total_points'] + 15
        elif action_type == 'vocab':
            updates['vocab_lookups'] = stats['vocab_lookups'] + 1
            updates['words_learned'] = stats['words_learned'] + 1
            updates['total_points'] = stats['total_points'] + 20
        
        # Update level (every 100 points = 1 level)
        if 'total_points' in updates:
            updates['level'] = (updates['total_points'] // 100) + 1
        
        # Apply updates
        if updates:
            supabase.table('user_stats').update(updates).eq('user_id', user['id']).execute()
        
        # Update streak
        try:
            update_streak(username)
        except Exception as streak_error:
            print(f"Error updating streak: {streak_error}")
        
        # Check for achievements
        try:
            check_achievements(username)
        except Exception as achievement_error:
            print(f"Error checking achievements: {achievement_error}")
        
        return True
    except Exception as e:
        print(f"Error in update_stats: {str(e)}")
        return False

def update_streak(username):
    """Update daily streak"""
    try:
        user = get_user_by_username(username)
        if not user:
            return
        
        stats_response = supabase.table('user_stats').select('*').eq('user_id', user['id']).execute()
        if not stats_response.data:
            return
        
        stats = stats_response.data[0]
        now = datetime.now()
        
        updates = {}
        
        if stats['last_activity']:
            last_activity = datetime.fromisoformat(stats['last_activity'])
            days_diff = (now.date() - last_activity.date()).days
            
            if days_diff == 0:
                # Same day, no change
                pass
            elif days_diff == 1:
                # Consecutive day, increase streak
                new_streak = stats['current_streak'] + 1
                updates['current_streak'] = new_streak
                if new_streak > stats['longest_streak']:
                    updates['longest_streak'] = new_streak
            else:
                # Streak broken
                updates['current_streak'] = 1
        else:
            updates['current_streak'] = 1
        
        updates['last_activity'] = now.isoformat()
        
        if updates:
            supabase.table('user_stats').update(updates).eq('user_id', user['id']).execute()
    except Exception as e:
        print(f"Error updating streak: {e}")

def check_achievements(username):
    """Check and award achievements"""
    try:
        user = get_user_by_username(username)
        if not user:
            return
        
        stats_response = supabase.table('user_stats').select('*').eq('user_id', user['id']).execute()
        if not stats_response.data:
            return
        
        stats = stats_response.data[0]
        
        # Get existing achievements
        existing_achievements = supabase.table('user_achievements').select('achievement_id').eq('user_id', user['id']).execute()
        achievement_ids = [a['achievement_id'] for a in existing_achievements.data] if existing_achievements.data else []
        
        # List of achievements
        possible_achievements = [
            {"id": "first_message", "name": "First Steps", "condition": stats['total_messages'] >= 1, "points": 50},
            {"id": "10_messages", "name": "Chatty Learner", "condition": stats['total_messages'] >= 10, "points": 100},
            {"id": "50_messages", "name": "Conversation Master", "condition": stats['total_messages'] >= 50, "points": 200},
            {"id": "grammar_5", "name": "Grammar Guru", "condition": stats['grammar_checks'] >= 5, "points": 75},
            {"id": "vocab_10", "name": "Word Collector", "condition": stats['words_learned'] >= 10, "points": 150},
            {"id": "streak_7", "name": "Week Warrior", "condition": stats['current_streak'] >= 7, "points": 300},
            {"id": "level_5", "name": "Level 5 Hero", "condition": stats['level'] >= 5, "points": 500},
        ]
        
        # Check and award new achievements
        points_to_add = 0
        for achievement in possible_achievements:
            if achievement['condition'] and achievement['id'] not in achievement_ids:
                # Award achievement
                supabase.table('user_achievements').insert({
                    "user_id": user['id'],
                    "achievement_id": achievement['id'],
                    "achievement_name": achievement['name'],
                    "earned_at": datetime.now().isoformat()
                }).execute()
                points_to_add += achievement['points']
        
        # Update total points if any achievements were earned
        if points_to_add > 0:
            supabase.table('user_stats').update({
                "total_points": stats['total_points'] + points_to_add
            }).eq('user_id', user['id']).execute()
            
    except Exception as e:
        print(f"Error checking achievements: {e}")

def get_progress(username):
    """Get user's progress data"""
    try:
        user = get_user_by_username(username)
        if not user:
            return None
        
        # Get stats
        stats_response = supabase.table('user_stats').select('*').eq('user_id', user['id']).execute()
        stats = stats_response.data[0] if stats_response.data else {}
        
        # Get recent activity
        history_response = supabase.table('chat_history').select('*').eq('user_id', user['id']).order('timestamp', desc=True).limit(10).execute()
        recent_activity = history_response.data if history_response.data else []
        
        return {
            "stats": stats,
            "recent_activity": recent_activity,
            "join_date": user.get('created_at'),
            "total_days": calculate_total_days(user.get('created_at'))
        }
    except Exception as e:
        print(f"Error getting progress: {e}")
        return None

def calculate_total_days(created_at):
    """Calculate days since account creation"""
    if not created_at:
        return 0
    created = datetime.fromisoformat(created_at)
    now = datetime.now()
    return (now.date() - created.date()).days + 1

def get_weekly_insights(username):
    """Generate weekly AI insights"""
    try:
        user = get_user_by_username(username)
        if not user:
            return None
        
        # Get stats
        stats_response = supabase.table('user_stats').select('*').eq('user_id', user['id']).execute()
        stats = stats_response.data[0] if stats_response.data else {}
        
        # Calculate this week's activity
        now = datetime.now()
        week_ago = now - timedelta(days=7)
        
        history_response = supabase.table('chat_history').select('*').eq('user_id', user['id']).gte('timestamp', week_ago.isoformat()).execute()
        weekly_messages = len(history_response.data) if history_response.data else 0
        
        # Get achievements count
        achievements_response = supabase.table('user_achievements').select('*').eq('user_id', user['id']).execute()
        achievements_count = len(achievements_response.data) if achievements_response.data else 0
        
        # Generate insights
        insights = {
            "week_summary": {
                "messages_sent": weekly_messages,
                "points_earned": stats.get('total_points', 0) % 100,  # Points this level
                "current_streak": stats.get('current_streak', 0),
                "level": stats.get('level', 1)
            },
            "achievements_unlocked": achievements_count,
            "total_words_learned": stats.get('words_learned', 0),
            "motivation": generate_motivation_message(stats)
        }
        
        return insights
    except Exception as e:
        print(f"Error getting weekly insights: {e}")
        return None

def generate_motivation_message(stats):
    """Generate personalized motivation message"""
    messages = stats.get('total_messages', 0)
    streak = stats.get('current_streak', 0)
    level = stats.get('level', 1)
    
    if streak >= 7:
        return f"🔥 Amazing! You're on a {streak}-day streak! Keep up the fantastic work!"
    elif messages >= 50:
        return f"🌟 You've sent {messages} messages! You're making incredible progress!"
    elif level >= 5:
        return f"🏆 Level {level}! You're becoming a language master!"
    else:
        return "💪 Keep learning! Every message brings you closer to fluency!"

def get_user_achievements(username):
    """Get all achievements earned by user"""
    try:
        user = get_user_by_username(username)
        if not user:
            return []
        
        achievements_response = supabase.table('user_achievements').select('*').eq('user_id', user['id']).order('earned_at', desc=True).execute()
        return achievements_response.data if achievements_response.data else []
    except Exception as e:
        print(f"Error getting user achievements: {e}")
        return []

def get_user_stats_only(username):
    """Get only user statistics without other data"""
    try:
        user = get_user_by_username(username)
        if not user:
            return None
        
        stats_response = supabase.table('user_stats').select('*').eq('user_id', user['id']).execute()
        return stats_response.data[0] if stats_response.data else None
    except Exception as e:
        print(f"Error getting user stats: {e}")
        return None