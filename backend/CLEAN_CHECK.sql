-- ============================================================
-- COPY & PASTE THIS INTO SUPABASE SQL EDITOR
-- ============================================================

-- CHECK 1: Verify all tables exist (should return 4)
SELECT COUNT(*) as tables_created 
FROM information_schema.tables
WHERE table_schema = 'public'
    AND table_name IN ('users', 'user_stats', 'chat_history', 'user_achievements');


-- CHECK 2: View current database summary
SELECT 
    (SELECT COUNT(*) FROM users) as total_users,
    (SELECT COUNT(*) FROM user_stats) as users_with_stats,
    (SELECT COUNT(*) FROM chat_history) as total_messages,
    (SELECT COUNT(*) FROM user_achievements) as achievements_earned;


-- CHECK 3: View all users with stats
SELECT 
    u.username,
    u.email,
    u.created_at,
    s.total_messages,
    s.total_points,
    s.level,
    s.current_streak,
    s.longest_streak
FROM users u
LEFT JOIN user_stats s ON u.id = s.user_id
ORDER BY u.created_at DESC;


-- CHECK 4: Recent chat history (last 10)
SELECT 
    u.username,
    ch.message,
    LEFT(ch.reply, 80) as reply,
    ch.timestamp
FROM chat_history ch
JOIN users u ON ch.user_id = u.id
ORDER BY ch.timestamp DESC
LIMIT 10;


-- CHECK 5: User leaderboard (top 10)
SELECT 
    ROW_NUMBER() OVER (ORDER BY s.total_points DESC) as rank,
    u.username,
    s.level,
    s.total_points,
    s.total_messages,
    s.current_streak
FROM users u
JOIN user_stats s ON u.id = s.user_id
ORDER BY s.total_points DESC
LIMIT 10;


-- CHECK 6: Achievements earned
SELECT 
    u.username,
    ua.achievement_name,
    ua.earned_at
FROM user_achievements ua
JOIN users u ON ua.user_id = u.id
ORDER BY ua.earned_at DESC;
