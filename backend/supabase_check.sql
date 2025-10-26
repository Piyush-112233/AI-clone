-- ============================================================
-- LinguaSpark AI - Database Verification & Testing Queries
-- ============================================================
-- Run these queries in Supabase SQL Editor to check your setup
-- ============================================================

-- ============================================================
-- 1. CHECK ALL TABLES EXIST
-- ============================================================
SELECT 
    table_name,
    table_type
FROM information_schema.tables
WHERE table_schema = 'public'
    AND table_name IN ('users', 'user_stats', 'chat_history', 'user_achievements')
ORDER BY table_name;

-- Expected: 4 rows (users, user_stats, chat_history, user_achievements)

-- ============================================================
-- 2. CHECK TABLE STRUCTURE
-- ============================================================

-- Users table columns
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'users'
ORDER BY ordinal_position;

-- User Stats table columns
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'user_stats'
ORDER BY ordinal_position;

-- Chat History table columns
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'chat_history'
ORDER BY ordinal_position;

-- User Achievements table columns
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'user_achievements'
ORDER BY ordinal_position;

-- ============================================================
-- 3. COUNT RECORDS IN EACH TABLE
-- ============================================================
SELECT 
    'users' as table_name, 
    COUNT(*) as total_records 
FROM users
UNION ALL
SELECT 
    'user_stats' as table_name, 
    COUNT(*) as total_records 
FROM user_stats
UNION ALL
SELECT 
    'chat_history' as table_name, 
    COUNT(*) as total_records 
FROM chat_history
UNION ALL
SELECT 
    'user_achievements' as table_name, 
    COUNT(*) as total_records 
FROM user_achievements
ORDER BY table_name;

-- ============================================================
-- 4. VIEW ALL USERS (WITH STATS)
-- ============================================================
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
    s.grammar_checks,
    s.vocab_lookups,
    s.last_activity
FROM users u
LEFT JOIN user_stats s ON u.id = s.user_id
ORDER BY u.created_at DESC;

-- ============================================================
-- 5. VIEW RECENT CHAT HISTORY (LAST 20)
-- ============================================================
SELECT 
    u.username,
    ch.message,
    LEFT(ch.reply, 100) as reply_preview,
    ch.timestamp
FROM chat_history ch
JOIN users u ON ch.user_id = u.id
ORDER BY ch.timestamp DESC
LIMIT 20;

-- ============================================================
-- 6. VIEW ALL ACHIEVEMENTS BY USER
-- ============================================================
SELECT 
    u.username,
    ua.achievement_id,
    ua.achievement_name,
    ua.earned_at
FROM user_achievements ua
JOIN users u ON ua.user_id = u.id
ORDER BY u.username, ua.earned_at DESC;

-- ============================================================
-- 7. USER LEADERBOARD (TOP 10 BY POINTS)
-- ============================================================
SELECT 
    ROW_NUMBER() OVER (ORDER BY s.total_points DESC) as rank,
    u.username,
    s.level,
    s.total_points,
    s.current_streak,
    s.total_messages,
    s.words_learned
FROM users u
JOIN user_stats s ON u.id = s.user_id
ORDER BY s.total_points DESC
LIMIT 10;

-- ============================================================
-- 8. ACTIVE USERS (LAST 7 DAYS)
-- ============================================================
SELECT 
    u.username,
    s.last_activity,
    s.current_streak,
    s.total_points
FROM users u
JOIN user_stats s ON u.id = s.user_id
WHERE s.last_activity >= NOW() - INTERVAL '7 days'
ORDER BY s.last_activity DESC;

-- ============================================================
-- 9. USER GROWTH STATS
-- ============================================================
SELECT 
    DATE(created_at) as signup_date,
    COUNT(*) as new_users
FROM users
GROUP BY DATE(created_at)
ORDER BY signup_date DESC
LIMIT 30;

-- ============================================================
-- 10. CHAT ACTIVITY BY USER
-- ============================================================
SELECT 
    u.username,
    COUNT(ch.id) as total_chats,
    MIN(ch.timestamp) as first_chat,
    MAX(ch.timestamp) as last_chat
FROM users u
LEFT JOIN chat_history ch ON u.id = ch.user_id
GROUP BY u.id, u.username
ORDER BY total_chats DESC;

-- ============================================================
-- 11. ACHIEVEMENT DISTRIBUTION
-- ============================================================
SELECT 
    achievement_id,
    achievement_name,
    COUNT(*) as users_earned,
    MIN(earned_at) as first_earned,
    MAX(earned_at) as last_earned
FROM user_achievements
GROUP BY achievement_id, achievement_name
ORDER BY users_earned DESC;

-- ============================================================
-- 12. DATABASE HEALTH CHECK
-- ============================================================
SELECT 
    'Total Users' as metric, 
    COUNT(*)::text as value 
FROM users
UNION ALL
SELECT 
    'Users with Stats' as metric, 
    COUNT(*)::text as value 
FROM user_stats
UNION ALL
SELECT 
    'Total Messages' as metric, 
    COUNT(*)::text as value 
FROM chat_history
UNION ALL
SELECT 
    'Total Achievements Earned' as metric, 
    COUNT(*)::text as value 
FROM user_achievements
UNION ALL
SELECT 
    'Active Today' as metric,
    COUNT(*)::text as value
FROM user_stats
WHERE last_activity::date = CURRENT_DATE;

-- ============================================================
-- 13. SEARCH SPECIFIC USER
-- ============================================================
-- Replace 'testuser' with actual username
SELECT 
    u.*,
    s.*,
    (SELECT COUNT(*) FROM chat_history WHERE user_id = u.id) as total_chats,
    (SELECT COUNT(*) FROM user_achievements WHERE user_id = u.id) as total_achievements
FROM users u
LEFT JOIN user_stats s ON u.id = s.user_id
WHERE u.username = 'testuser';

-- ============================================================
-- 14. DELETE SPECIFIC USER (AND ALL THEIR DATA)
-- ============================================================
-- ⚠️ DANGER: This will delete user and all related data!
-- Uncomment and replace 'testuser' to use:
-- DELETE FROM users WHERE username = 'testuser';

-- ============================================================
-- 15. CLEAN FORM: ESSENTIAL CHECKS ONLY
-- ============================================================
-- Quick verification - run this first after setup

-- Check tables exist
SELECT COUNT(*) as tables_created 
FROM information_schema.tables
WHERE table_schema = 'public'
    AND table_name IN ('users', 'user_stats', 'chat_history', 'user_achievements');
-- Expected: 4

-- Check RLS is enabled
SELECT 
    tablename,
    rowsecurity as rls_enabled
FROM pg_tables
WHERE schemaname = 'public'
    AND tablename IN ('users', 'user_stats', 'chat_history', 'user_achievements')
ORDER BY tablename;
-- Expected: All should show 't' (true)

-- Quick summary
SELECT 
    (SELECT COUNT(*) FROM users) as total_users,
    (SELECT COUNT(*) FROM user_stats) as users_with_stats,
    (SELECT COUNT(*) FROM chat_history) as total_messages,
    (SELECT COUNT(*) FROM user_achievements) as achievements_earned;

-- ============================================================
-- ✅ ALL CHECKS COMPLETE!
-- ============================================================
