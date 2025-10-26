// Enhanced State Management for LinguaSpark AI
// This file provides persistent state management using localStorage

class StateManager {
    constructor() {
        this.storageKey = 'linguaspark_state';
        this.state = this.loadState();
    }

    // Load state from localStorage
    loadState() {
        try {
            const saved = localStorage.getItem(this.storageKey);
            return saved ? JSON.parse(saved) : this.getDefaultState();
        } catch (error) {
            console.error('Error loading state:', error);
            return this.getDefaultState();
        }
    }

    // Get default state structure
    getDefaultState() {
        return {
            user: {
                username: null,
                email: null,
                lastLogin: null
            },
            preferences: {
                userLang: 'English',
                targetLang: 'Spanish',
                theme: 'light',
                notifications: true
            },
            chatHistory: [],
            stats: {
                totalMessages: 0,
                languagesLearned: [],
                joinDate: new Date().toISOString()
            }
        };
    }

    // Save state to localStorage
    saveState() {
        try {
            localStorage.setItem(this.storageKey, JSON.stringify(this.state));
        } catch (error) {
            console.error('Error saving state:', error);
        }
    }

    // User management
    setUser(username, email) {
        this.state.user = {
            username,
            email,
            lastLogin: new Date().toISOString()
        };
        this.saveState();
    }

    getUser() {
        return this.state.user;
    }

    clearUser() {
        this.state.user = this.getDefaultState().user;
        this.saveState();
    }

    // Preferences management
    setPreference(key, value) {
        this.state.preferences[key] = value;
        this.saveState();
    }

    getPreference(key) {
        return this.state.preferences[key];
    }

    setLanguages(userLang, targetLang) {
        this.state.preferences.userLang = userLang;
        this.state.preferences.targetLang = targetLang;
        
        // Track languages learned
        if (!this.state.stats.languagesLearned.includes(targetLang)) {
            this.state.stats.languagesLearned.push(targetLang);
        }
        
        this.saveState();
    }

    // Chat history management
    addChatMessage(userMessage, botReply) {
        const message = {
            id: Date.now(),
            user: userMessage,
            bot: botReply,
            timestamp: new Date().toISOString(),
            languages: {
                from: this.state.preferences.userLang,
                to: this.state.preferences.targetLang
            }
        };

        this.state.chatHistory.unshift(message);
        
        // Keep only last 100 messages
        if (this.state.chatHistory.length > 100) {
            this.state.chatHistory = this.state.chatHistory.slice(0, 100);
        }

        // Update stats
        this.state.stats.totalMessages++;
        
        this.saveState();
    }

    getChatHistory(limit = 50) {
        return this.state.chatHistory.slice(0, limit);
    }

    clearChatHistory() {
        this.state.chatHistory = [];
        this.saveState();
    }

    // Statistics
    getStats() {
        return {
            ...this.state.stats,
            messagesCount: this.state.chatHistory.length,
            daysActive: this.calculateDaysActive()
        };
    }

    calculateDaysActive() {
        const joinDate = new Date(this.state.stats.joinDate);
        const now = new Date();
        const diffTime = Math.abs(now - joinDate);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        return diffDays;
    }

    // Export data
    exportData() {
        return {
            ...this.state,
            exportDate: new Date().toISOString()
        };
    }

    // Import data
    importData(data) {
        try {
            this.state = {
                ...this.getDefaultState(),
                ...data
            };
            this.saveState();
            return true;
        } catch (error) {
            console.error('Error importing data:', error);
            return false;
        }
    }

    // Clear all data
    clearAll() {
        localStorage.removeItem(this.storageKey);
        this.state = this.getDefaultState();
    }
}

// Create global state manager instance
const stateManager = new StateManager();

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = StateManager;
}
