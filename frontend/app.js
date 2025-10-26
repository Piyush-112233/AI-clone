const API_URL = 'http://127.0.0.1:8000';
let currentUser = null;
let userStats = null;

// ============ AUTH FUNCTIONS ============

function showSignup() {
    document.getElementById('loginForm').style.display = 'none';
    document.getElementById('signupForm').style.display = 'block';
    document.getElementById('authMessage').innerHTML = '';
}

function showLogin() {
    document.getElementById('signupForm').style.display = 'none';
    document.getElementById('loginForm').style.display = 'block';
    document.getElementById('authMessage').innerHTML = '';
}

async function signup() {
    const username = document.getElementById('signupUsername').value.trim();
    const email = document.getElementById('signupEmail').value.trim();
    const password = document.getElementById('signupPassword').value;

    if (!username || !email || !password) {
        showAuthMessage('❌ Please fill all fields', 'error');
        return;
    }

    if (password.length < 6) {
        showAuthMessage('❌ Password must be at least 6 characters', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/signup`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })
        });

        const data = await response.json();

        if (response.ok) {
            showAuthMessage('✅ Account created! Please login.', 'success');
            setTimeout(showLogin, 2000);
        } else {
            showAuthMessage(`❌ ${data.detail}`, 'error');
        }
    } catch (error) {
        showAuthMessage('❌ Connection error. Is the server running?', 'error');
    }
}

async function login() {
    const username = document.getElementById('loginUsername').value.trim();
    const password = document.getElementById('loginPassword').value;

    if (!username || !password) {
        showAuthMessage('❌ Please enter username and password', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (response.ok) {
            currentUser = data.user.username;
            userStats = data.user.stats;
            localStorage.setItem('linguaspark_user', currentUser);
            showChatScreen();
            updateProgressBar(); // 🆕 NEW: Update progress display
            loadUserProgress(); // 🆕 NEW: Load user stats
        } else {
            showAuthMessage(`❌ ${data.detail}`, 'error');
        }
    } catch (error) {
        showAuthMessage('❌ Connection error. Is the server running?', 'error');
    }
}

function logout() {
    currentUser = null;
    userStats = null;
    localStorage.removeItem('linguaspark_user');
    document.getElementById('chatScreen').style.display = 'none';
    document.getElementById('authScreen').style.display = 'flex';
    document.getElementById('chatBox').innerHTML = `
        <div class="welcome-message">
            <h3>👋 Welcome to LinguaSpark!</h3>
            <p>Start learning and earn XP! Complete challenges, check grammar, learn vocabulary!</p>
            <p class="hint">💡 Each message = 10 XP | Grammar check = 15 XP | Vocabulary = 20 XP</p>
        </div>
    `;
}

function showChatScreen() {
    document.getElementById('authScreen').style.display = 'none';
    document.getElementById('chatScreen').style.display = 'flex';
    document.getElementById('usernameDisplay').textContent = `👤 ${currentUser}`;
    document.getElementById('userInput').focus();
}

function showAuthMessage(message, type) {
    const msgDiv = document.getElementById('authMessage');
    msgDiv.innerHTML = message;
    msgDiv.className = `auth-message ${type}`;
}

// ============ 🆕 NEW: PROGRESS & STATS FUNCTIONS ============

async function loadUserProgress() {
    /**
     * Load user's progress from backend
     * Updates XP bar, streak, achievements
     */
    try {
        const response = await fetch(`${API_URL}/progress/${currentUser}`);
        const data = await response.json();
        
        if (response.ok && data.stats) {
            userStats = data.stats;
            updateProgressBar();
            updateFooterStats();
        } else {
            console.warn('Stats not available, using defaults');
            // Initialize with default values if stats are missing
            userStats = {
                total_messages: 0,
                words_learned: 0,
                current_streak: 0,
                total_points: 0,
                level: 1,
                achievements: []
            };
            updateProgressBar();
            updateFooterStats();
        }
    } catch (error) {
        console.error('Error loading progress:', error);
        // Set default values on error to prevent UI breaking
        userStats = {
            total_messages: 0,
            words_learned: 0,
            current_streak: 0,
            total_points: 0,
            level: 1,
            achievements: []
        };
        updateProgressBar();
        updateFooterStats();
    }
}

function updateProgressBar() {
    /**
     * Update the XP progress bar display
     * Shows level, points, and progress percentage
     */
    if (!userStats) return;
    
    const level = userStats.level || 1;
    const totalPoints = userStats.total_points || 0;
    const pointsInLevel = totalPoints % 100;
    const nextLevel = level * 100;
    const percentage = (pointsInLevel / 100) * 100;
    
    // Safely update elements if they exist
    const userLevelEl = document.getElementById('userLevel');
    const userPointsEl = document.getElementById('userPoints');
    const nextLevelPointsEl = document.getElementById('nextLevelPoints');
    const progressFillEl = document.getElementById('progressFill');
    
    if (userLevelEl) userLevelEl.textContent = level;
    if (userPointsEl) userPointsEl.textContent = pointsInLevel;
    if (nextLevelPointsEl) nextLevelPointsEl.textContent = 100;
    if (progressFillEl) progressFillEl.style.width = `${percentage}%`;
}

function updateFooterStats() {
    /**
     * Update footer with streak and achievements
     */
    if (!userStats) return;
    
    const streakEl = document.getElementById('streakDays');
    const achievementEl = document.getElementById('achievementCount');
    
    if (streakEl) {
        streakEl.textContent = userStats.current_streak || 0;
    }
    if (achievementEl) {
        achievementEl.textContent = (userStats.achievements || []).length;
    }
}

function showXPGain(points) {
    /**
     * Show animated XP gain notification
     * Displays "+X XP" popup that floats up
     */
    const notification = document.createElement('div');
    notification.className = 'xp-notification';
    notification.innerHTML = `+${points} XP 🌟`;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateY(-100px)';
    }, 100);
    
    setTimeout(() => {
        notification.remove();
    }, 2000);
}

function checkLevelUp(oldPoints, newPoints) {
    /**
     * Check if user leveled up
     * Show celebration if they did!
     */
    const oldLevel = Math.floor(oldPoints / 100) + 1;
    const newLevel = Math.floor(newPoints / 100) + 1;
    
    if (newLevel > oldLevel) {
        showLevelUpCelebration(newLevel);
    }
}

function showLevelUpCelebration(level) {
    /**
     * Show level up celebration animation
     */
    const celebration = document.createElement('div');
    celebration.className = 'level-up-celebration';
    celebration.innerHTML = `
        <div class="celebration-content">
            <h2>🎉 LEVEL UP! 🎉</h2>
            <p class="level-text">Level ${level}</p>
            <p>You're becoming a language master!</p>
        </div>
    `;
    document.body.appendChild(celebration);
    
    setTimeout(() => {
        celebration.style.opacity = '0';
    }, 3000);
    
    setTimeout(() => {
        celebration.remove();
    }, 3500);
}

// ============ CHAT FUNCTIONS ============

async function sendMessage() {
    const userInput = document.getElementById('userInput');
    const chatBox = document.getElementById('chatBox');
    const sendBtn = document.getElementById('sendBtn');
    const message = userInput.value.trim();

    if (!message) {
        alert('⚠️ Please type a message!');
        return;
    }

    if (!currentUser) {
        alert('⚠️ Please login first!');
        return;
    }

    const userLang = document.getElementById('userLang').value;
    const targetLang = document.getElementById('targetLang').value;

    // Remove welcome message
    const welcomeMsg = chatBox.querySelector('.welcome-message');
    if (welcomeMsg) welcomeMsg.remove();

    // Display user message
    addMessage('user', message);
    userInput.value = '';
    
    // Disable input
    sendBtn.disabled = true;
    sendBtn.innerHTML = '<span>Thinking...</span><span class="spinner">⏳</span>';

    // Show typing indicator
    const typingId = addTypingIndicator();

    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username: currentUser,
                text: message,
                user_lang: userLang,
                target_lang: targetLang
            })
        });

        const data = await response.json();
        
        removeTypingIndicator(typingId);

        if (response.ok) {
            addMessage('bot', data.reply);
            
            // 🆕 NEW: Show XP gain and update progress
            const oldPoints = userStats?.total_points || 0;
            showXPGain(10);
            await loadUserProgress();
            checkLevelUp(oldPoints, userStats?.total_points || 0);
        } else {
            addMessage('error', `❌ ${data.detail || 'Error occurred'}`);
        }

    } catch (error) {
        removeTypingIndicator(typingId);
        addMessage('error', `❌ Connection Error: ${error.message}`);
    } finally {
        sendBtn.disabled = false;
        sendBtn.innerHTML = '<span>Send</span><span class="icon">➤</span>';
        userInput.focus();
    }
}

// ============ GRAMMAR CHECK FUNCTIONS ============

function showGrammarCheck() {
    document.getElementById('grammarModal').style.display = 'flex';
    document.getElementById('grammarInput').value = '';
    document.getElementById('grammarResult').innerHTML = '';
}

function closeGrammarCheck() {
    document.getElementById('grammarModal').style.display = 'none';
}

async function checkGrammar() {
    const text = document.getElementById('grammarInput').value.trim();
    const resultDiv = document.getElementById('grammarResult');

    if (!text) {
        resultDiv.innerHTML = '<p class="error">⚠️ Please enter a sentence!</p>';
        return;
    }

    resultDiv.innerHTML = '<p class="loading">🔍 Checking grammar...</p>';

    try {
        const response = await fetch(`${API_URL}/grammar-check`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username: currentUser,
                text: text,
                language: document.getElementById('userLang').value
            })
        });

        const data = await response.json();

        if (data.error) {
            resultDiv.innerHTML = `<p class="error">❌ ${data.error}</p>`;
        } else {
            resultDiv.innerHTML = `
                <div class="grammar-result">
                    <h3>📝 Your Text:</h3>
                    <p class="original-text">${data.original}</p>
                    <h3>✅ Analysis:</h3>
                    <div class="analysis">${formatBotResponse(data.analysis)}</div>
                </div>
            `;
            
            // 🆕 NEW: Show XP gain
            const oldPoints = userStats?.total_points || 0;
            showXPGain(15);
            await loadUserProgress();
            checkLevelUp(oldPoints, userStats?.total_points || 0);
        }

    } catch (error) {
        resultDiv.innerHTML = `<p class="error">❌ Connection Error: ${error.message}</p>`;
    }
}

// ============ VOCABULARY FUNCTIONS ============

function showVocabulary() {
    document.getElementById('vocabModal').style.display = 'flex';
    document.getElementById('vocabInput').value = '';
    document.getElementById('vocabResult').innerHTML = '';
}

function closeVocabulary() {
    document.getElementById('vocabModal').style.display = 'none';
}

async function explainVocabulary() {
    const word = document.getElementById('vocabInput').value.trim();
    const resultDiv = document.getElementById('vocabResult');

    if (!word) {
        resultDiv.innerHTML = '<p class="error">⚠️ Please enter a word!</p>';
        return;
    }

    resultDiv.innerHTML = '<p class="loading">📖 Looking up word...</p>';

    try {
        const response = await fetch(`${API_URL}/vocabulary`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username: currentUser,
                word: word,
                language: document.getElementById('targetLang').value
            })
        });

        const data = await response.json();

        if (data.error) {
            resultDiv.innerHTML = `<p class="error">❌ ${data.error}</p>`;
        } else {
            resultDiv.innerHTML = `
                <div class="vocab-result">
                    <h3>📚 Word: <span class="highlight">${data.word}</span></h3>
                    <h4>Language: ${data.language}</h4>
                    <div class="explanation">${formatBotResponse(data.explanation)}</div>
                </div>
            `;
            
            // 🆕 NEW: Show XP gain
            const oldPoints = userStats?.total_points || 0;
            showXPGain(20);
            await loadUserProgress();
            checkLevelUp(oldPoints, userStats?.total_points || 0);
        }

    } catch (error) {
        resultDiv.innerHTML = `<p class="error">❌ Connection Error: ${error.message}</p>`;
    }
}

// ============ 🆕 NEW: DASHBOARD FUNCTIONS ============

async function showDashboard() {
    /**
     * Show the progress dashboard modal
     * Loads all stats, achievements, and weekly insights
     */
    document.getElementById('dashboardModal').style.display = 'flex';
    
    // Load fresh data
    await loadDashboardData();
}

function closeDashboard() {
    document.getElementById('dashboardModal').style.display = 'none';
}

async function loadDashboardData() {
    /**
     * Load all dashboard data from backend
     * Populates stats, achievements, and insights
     */
    try {
        // Load progress data
        const progressResponse = await fetch(`${API_URL}/progress/${currentUser}`);
        const progressData = await progressResponse.json();
        
        if (progressResponse.ok && progressData.stats) {
            updateDashboardStats(progressData.stats);
            updateDashboardAchievements(progressData.stats.achievements || []);
        } else {
            console.warn('Progress data not available');
            // Set default empty stats
            updateDashboardStats({
                total_messages: 0,
                words_learned: 0,
                level: 1,
                current_streak: 0
            });
            updateDashboardAchievements([]);
        }
        
        // Load weekly insights
        const insightsResponse = await fetch(`${API_URL}/weekly-insights/${currentUser}`);
        const insightsData = await insightsResponse.json();
        
        if (insightsResponse.ok && insightsData) {
            updateWeeklyInsights(insightsData);
        } else {
            console.warn('Insights not available');
            // Show default insights
            document.getElementById('weeklyInsights').innerHTML = `
                <div class="insights-content">
                    <h4>📊 Welcome to Your Dashboard!</h4>
                    <p>Start chatting to see your weekly progress and insights here.</p>
                </div>
            `;
        }
        
    } catch (error) {
        console.error('Error loading dashboard:', error);
        // Show user-friendly error message
        document.getElementById('weeklyInsights').innerHTML = `
            <div class="insights-content">
                <h4>⚠️ Unable to Load Data</h4>
                <p>Please check your connection and try again.</p>
            </div>
        `;
    }
}

function updateDashboardStats(stats) {
    /**
     * Update the statistics cards in dashboard
     */
    const elements = {
        dashTotalMessages: document.getElementById('dashTotalMessages'),
        dashWordsLearned: document.getElementById('dashWordsLearned'),
        dashLevel: document.getElementById('dashLevel'),
        dashStreak: document.getElementById('dashStreak')
    };
    
    // Safely update each element if it exists
    if (elements.dashTotalMessages) {
        elements.dashTotalMessages.textContent = stats.total_messages || 0;
    }
    if (elements.dashWordsLearned) {
        elements.dashWordsLearned.textContent = stats.words_learned || 0;
    }
    if (elements.dashLevel) {
        elements.dashLevel.textContent = stats.level || 1;
    }
    if (elements.dashStreak) {
        elements.dashStreak.textContent = stats.current_streak || 0;
    }
}

function updateDashboardAchievements(achievements) {
    /**
     * Display all unlocked achievements
     */
    const achievementsList = document.getElementById('achievementsList');
    
    // All possible achievements
    const allAchievements = {
        "first_message": { name: "First Steps", icon: "👶", description: "Sent your first message" },
        "10_messages": { name: "Chatty Learner", icon: "💬", description: "Sent 10 messages" },
        "50_messages": { name: "Conversation Master", icon: "🎯", description: "Sent 50 messages" },
        "grammar_5": { name: "Grammar Guru", icon: "✅", description: "5 grammar checks" },
        "vocab_10": { name: "Word Collector", icon: "📚", description: "Learned 10 words" },
        "streak_7": { name: "Week Warrior", icon: "🔥", description: "7-day streak" },
        "level_5": { name: "Level 5 Hero", icon: "🏆", description: "Reached level 5" }
    };
    
    if (achievements.length === 0) {
        achievementsList.innerHTML = '<p class="no-achievements">🎯 Complete activities to unlock achievements!</p>';
        return;
    }
    
    achievementsList.innerHTML = achievements.map(id => {
        const achievement = allAchievements[id];
        if (!achievement) return '';
        
        return `
            <div class="achievement-card unlocked">
                <div class="achievement-icon">${achievement.icon}</div>
                <div class="achievement-info">
                    <h4>${achievement.name}</h4>
                    <p>${achievement.description}</p>
                </div>
            </div>
        `;
    }).join('');
}

function updateWeeklyInsights(insights) {
    /**
     * Display AI-generated weekly insights
     */
    const insightsBox = document.getElementById('weeklyInsights');
    
    // Handle missing or incomplete data gracefully
    if (!insights || !insights.week_summary) {
        insightsBox.innerHTML = `
            <div class="insights-content">
                <h4>📊 Weekly Insights</h4>
                <p>Keep learning to see your weekly progress summary!</p>
            </div>
        `;
        return;
    }
    
    const summary = insights.week_summary;
    
    insightsBox.innerHTML = `
        <div class="insights-content">
            <h4>📊 This Week's Summary</h4>
            <div class="insight-item">
                <span class="insight-icon">💬</span>
                <span>You sent <strong>${summary.messages_sent || 0}</strong> messages</span>
            </div>
            <div class="insight-item">
                <span class="insight-icon">⭐</span>
                <span>Earned <strong>${summary.points_earned || 0}</strong> XP</span>
            </div>
            <div class="insight-item">
                <span class="insight-icon">🔥</span>
                <span><strong>${summary.current_streak || 0}</strong> day streak</span>
            </div>
            <div class="insight-item">
                <span class="insight-icon">🏆</span>
                <span>Level <strong>${summary.level || 1}</strong></span>
            </div>
            <div class="motivation-message">
                <p>${insights.motivation || 'Keep up the great work!'}</p>
            </div>
            <div class="insight-stats">
                <p><strong>🏅 Achievements Unlocked:</strong> ${insights.achievements_unlocked || 0}</p>
                <p><strong>📚 Total Words Learned:</strong> ${insights.total_words_learned || 0}</p>
            </div>
        </div>
    `;
}

// ============ HELPER FUNCTIONS ============

// ============ HELPER FUNCTIONS ============

function addMessage(type, text) {
    const chatBox = document.getElementById('chatBox');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    
    if (type === 'user') {
        messageDiv.innerHTML = `
            <div class="message-content">
                <strong>You:</strong>
                <p>${escapeHtml(text)}</p>
            </div>
        `;
    } else if (type === 'bot') {
        messageDiv.innerHTML = `
            <div class="message-content">
                <strong>🌟 LinguaSpark:</strong>
                <p>${formatBotResponse(text)}</p>
            </div>
        `;
    } else if (type === 'error') {
        messageDiv.innerHTML = `
            <div class="message-content">
                <strong>⚠️ Error:</strong>
                <p>${text}</p>
            </div>
        `;
    }
    
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function addTypingIndicator() {
    const chatBox = document.getElementById('chatBox');
    const typingDiv = document.createElement('div');
    const id = 'typing_' + Date.now();
    typingDiv.id = id;
    typingDiv.className = 'message bot-message typing-indicator';
    typingDiv.innerHTML = `
        <div class="message-content">
            <strong>🌟 LinguaSpark:</strong>
            <p><span class="dot"></span><span class="dot"></span><span class="dot"></span></p>
        </div>
    `;
    chatBox.appendChild(typingDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
    return id;
}

function removeTypingIndicator(id) {
    const element = document.getElementById(id);
    if (element) element.remove();
}

function formatBotResponse(text) {
    return text
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ============ CHECK LOGIN ON PAGE LOAD ============

window.addEventListener('load', async () => {
    const savedUser = localStorage.getItem('linguaspark_user');
    if (savedUser) {
        currentUser = savedUser;
        showChatScreen();
        await loadUserProgress();
    }
});

// Close modals when clicking outside
window.onclick = function(event) {
    if (event.target.className === 'modal') {
        event.target.style.display = 'none';
    }
}