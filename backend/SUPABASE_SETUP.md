# 🗄️ Supabase Database Setup Guide

## 📋 Quick Setup Steps

### 1️⃣ Create Supabase Project
1. Go to [https://app.supabase.com/](https://app.supabase.com/)
2. Click **"New Project"**
3. Fill in:
   - **Project name**: LinguaSpark-AI
   - **Database password**: (create a strong password)
   - **Region**: Choose closest to your users
4. Click **"Create new project"**
5. Wait 2-3 minutes for setup to complete

### 2️⃣ Run Database Setup Script
1. In your Supabase dashboard, click **"SQL Editor"** (left sidebar)
2. Click **"New Query"**
3. Copy & paste the entire contents of **`supabase_setup.sql`**
4. Click **"Run"** (or press Ctrl+Enter)
5. ✅ You should see "Success. No rows returned"

### 3️⃣ Get Your Credentials
1. Click **"Project Settings"** (gear icon, bottom left)
2. Click **"API"** in the settings menu
3. Copy these values:
   - **Project URL** → This is your `SUPABASE_URL`
   - **anon public** key → This is your `SUPABASE_KEY`

### 4️⃣ Configure Environment Variables
1. In your backend folder, create a `.env` file
2. Add your credentials:
```env
GROQ_API_KEY=your_groq_api_key_here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key_here
```

### 5️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 6️⃣ Verify Setup
1. Go back to Supabase **SQL Editor**
2. Copy & paste this quick check:
```sql
SELECT COUNT(*) as tables_created 
FROM information_schema.tables
WHERE table_schema = 'public'
    AND table_name IN ('users', 'user_stats', 'chat_history', 'user_achievements');
```
3. Expected result: **4** (all tables created)

---

## 🔍 Database Verification Queries

Use **`supabase_check.sql`** for comprehensive database testing. Here are the most useful queries:

### ✅ Check All Tables Exist
```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
    AND table_name IN ('users', 'user_stats', 'chat_history', 'user_achievements')
ORDER BY table_name;
```

### 👥 View All Users
```sql
SELECT 
    u.username,
    u.email,
    u.created_at,
    s.total_points,
    s.level,
    s.current_streak
FROM users u
LEFT JOIN user_stats s ON u.id = s.user_id
ORDER BY u.created_at DESC;
```

### 💬 Recent Chat History
```sql
SELECT 
    u.username,
    ch.message,
    LEFT(ch.reply, 100) as reply_preview,
    ch.timestamp
FROM chat_history ch
JOIN users u ON ch.user_id = u.id
ORDER BY ch.timestamp DESC
LIMIT 20;
```

### 📊 Quick Summary
```sql
SELECT 
    (SELECT COUNT(*) FROM users) as total_users,
    (SELECT COUNT(*) FROM chat_history) as total_messages,
    (SELECT COUNT(*) FROM user_achievements) as achievements_earned;
```

---

## 🗂️ Database Schema

### **users** table
- `id` (UUID) - Primary key
- `username` (TEXT) - Unique username
- `email` (TEXT) - Unique email
- `password` (TEXT) - Hashed password
- `created_at` (TIMESTAMPTZ) - Account creation date

### **user_stats** table
- `id` (UUID) - Primary key
- `user_id` (UUID) - Foreign key → users
- `total_messages` (INTEGER) - Messages sent
- `words_learned` (INTEGER) - Words learned
- `grammar_checks` (INTEGER) - Grammar checks done
- `vocab_lookups` (INTEGER) - Vocabulary lookups
- `current_streak` (INTEGER) - Current daily streak
- `longest_streak` (INTEGER) - Longest streak achieved
- `last_activity` (TIMESTAMPTZ) - Last activity timestamp
- `total_points` (INTEGER) - Total points earned
- `level` (INTEGER) - User level

### **chat_history** table
- `id` (UUID) - Primary key
- `user_id` (UUID) - Foreign key → users
- `message` (TEXT) - User's message
- `reply` (TEXT) - AI's reply
- `timestamp` (TIMESTAMPTZ) - Message timestamp

### **user_achievements** table
- `id` (UUID) - Primary key
- `user_id` (UUID) - Foreign key → users
- `achievement_id` (TEXT) - Achievement identifier
- `achievement_name` (TEXT) - Achievement name
- `earned_at` (TIMESTAMPTZ) - When earned

---

## 🔒 Security Features

✅ **Row Level Security (RLS)** enabled on all tables  
✅ **Policies** configured for data access control  
✅ **Automatic timestamps** with triggers  
✅ **Cascade delete** - deleting user removes all their data  
✅ **Unique constraints** on username and email  

---

## 🧪 Testing Your Setup

### Test 1: Create a User (via API)
```bash
curl -X POST http://localhost:8000/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"test123"}'
```

### Test 2: Check User in Database
```sql
SELECT * FROM users WHERE username = 'testuser';
```

### Test 3: Check User Stats Created
```sql
SELECT u.username, s.* 
FROM users u
JOIN user_stats s ON u.id = s.user_id
WHERE u.username = 'testuser';
```

---

## 🛠️ Useful Maintenance Queries

### Delete All Test Data
```sql
DELETE FROM users WHERE username LIKE 'test%';
```

### Reset User Stats
```sql
UPDATE user_stats 
SET total_messages = 0, 
    total_points = 0, 
    level = 1,
    current_streak = 0
WHERE user_id = (SELECT id FROM users WHERE username = 'testuser');
```

### Clean Old Chat History (keep last 50 per user)
```sql
SELECT cleanup_old_chat_history();
```

---

## 📝 Migration from JSON to Supabase

If you have existing users in `users.json`, you'll need to migrate them manually or create a migration script. The new structure is:

**Old (JSON):**
```json
{
  "username": {
    "email": "...",
    "password": "...",
    "stats": {...},
    "chat_history": [...]
  }
}
```

**New (Supabase):**
- Separate tables for users, stats, history, achievements
- Relational structure with foreign keys
- Better performance and scalability

---

## ❓ Troubleshooting

### Error: "SUPABASE_URL and SUPABASE_KEY must be set"
- Check your `.env` file exists in backend folder
- Verify the variable names match exactly
- Restart your server after adding .env variables

### Error: "relation 'users' does not exist"
- Run the setup script (`supabase_setup.sql`) in SQL Editor
- Check you're in the correct project
- Verify tables with: `SELECT * FROM information_schema.tables WHERE table_schema = 'public';`

### Error: "new row violates row-level security policy"
- RLS policies might be too restrictive
- For testing, you can temporarily disable RLS:
  ```sql
  ALTER TABLE users DISABLE ROW LEVEL SECURITY;
  ```
- Re-enable after testing:
  ```sql
  ALTER TABLE users ENABLE ROW LEVEL SECURITY;
  ```

---

## 🎉 You're All Set!

Your Supabase database is now configured and ready for LinguaSpark AI!

**Next Steps:**
1. Start your backend: `uvicorn main:app --reload`
2. Test signup/login endpoints
3. Monitor your database in Supabase dashboard
4. Use `supabase_check.sql` to verify everything works

**Dashboard Access:**
- View data: Table Editor
- Run queries: SQL Editor
- Monitor: Logs section
- Settings: Project Settings

---

**Need Help?**
- [Supabase Documentation](https://supabase.com/docs)
- [Supabase Discord](https://discord.supabase.com/)
