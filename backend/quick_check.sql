-- ============================================================
-- 🚀 QUICK CHECK - Run this first in Supabase SQL Editor
-- ============================================================

-- 1. Count tables (should be 4)
SELECT COUNT(*) as tables_created 
FROM information_schema.tables
WHERE table_schema = 'public'
    AND table_name IN ('users', 'user_stats', 'chat_history', 'user_achievements');

-- 2. Check RLS is enabled (all should show 't')
SELECT 
    tablename,
    rowsecurity as rls_enabled
FROM pg_tables
WHERE schemaname = 'public'
    AND tablename IN ('users', 'user_stats', 'chat_history', 'user_achievements')
ORDER BY tablename;

-- 3. Quick summary of all data
SELECT 
    (SELECT COUNT(*) FROM users) as total_users,
    (SELECT COUNT(*) FROM user_stats) as users_with_stats,
    (SELECT COUNT(*) FROM chat_history) as total_messages,
    (SELECT COUNT(*) FROM user_achievements) as achievements_earned;

-- 4. View all users with their stats
SELECT 
    u.id,
    u.username,
    u.email,
    u.created_at,
    s.total_messages,
    s.total_points,
    s.level,
    s.current_streak,
    s.longest_streak,
    s.words_learned,
    s.last_activity
FROM users u
LEFT JOIN user_stats s ON u.id = s.user_id
ORDER BY u.created_at DESC;

-- 5. View recent chat history (last 10)
SELECT 
    u.username,
    ch.message,
    LEFT(ch.reply, 80) as reply_preview,
    ch.timestamp
FROM chat_history ch
JOIN users u ON ch.user_id = u.id
ORDER BY ch.timestamp DESC
LIMIT 10;

-- 6. View all achievements earned
SELECT 
    u.username,
    ua.achievement_name,
    ua.achievement_id,
    ua.earned_at
FROM user_achievements ua
JOIN users u ON ua.user_id = u.id
ORDER BY ua.earned_at DESC;

-- 7. Leaderboard (top users by points)
SELECT 
    ROW_NUMBER() OVER (ORDER BY s.total_points DESC) as rank,
    u.username,
    s.level,
    s.total_points,
    s.current_streak,
    s.total_messages
FROM users u
JOIN user_stats s ON u.id = s.user_id
ORDER BY s.total_points DESC
LIMIT 10;

-- ============================================================
-- 🧹 CLEANUP QUERIES (Use carefully!)
-- ============================================================

-- Delete test users (uncomment to use)
-- DELETE FROM users WHERE username LIKE 'test%';

-- Delete specific user (uncomment and replace username)
-- DELETE FROM users WHERE username = 'testuser';

-- Reset all data (⚠️ DANGER - deletes everything!)
-- TRUNCATE users, user_stats, chat_history, user_achievements CASCADE;
