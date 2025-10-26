# LinguaSpark AI 🌟

## Learn Languages Naturally with AI

LinguaSpark is an AI-powered language learning platform that helps you learn new languages through natural conversation. Using advanced AI (Groq's Llama 3.3), it provides real-time translations, contextual explanations, and personalized teaching.

---

## ✨ Features

- 🤖 **AI-Powered Teaching** - Natural language learning with Groq's Llama 3.3 70B
- 🌍 **10+ Languages** - English, Spanish, French, German, Italian, Portuguese, Chinese, Japanese, Korean, Hindi
- 💬 **Real-time Chat** - Instant translations and explanations
- 🔐 **Secure Authentication** - User accounts with encrypted passwords
- 📚 **Chat History** - Save and review your learning progress
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile
- 🆓 **100% Free** - No hidden costs, no ads

---

## 🚀 Tech Stack

### Frontend
- HTML5, CSS3, Vanilla JavaScript
- Responsive design with modern animations
- LocalStorage for session management

### Backend
- **Framework:** FastAPI (Python)
- **AI Model:** Groq Llama 3.3 70B Versatile
- **Authentication:** Password hashing (SHA-256)
- **Database:** JSON-based (users.json)
- **API:** RESTful with CORS enabled

### Dependencies
- `fastapi` - Modern web framework
- `uvicorn` - ASGI server
- `groq` - AI/LLM API client
- `pydantic` - Data validation
- `python-dotenv` - Environment management

---

## 📦 Installation

### Prerequisites
- Python 3.10+
- Free Groq API key ([Get one here](https://console.groq.com))

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/linguaspark-ai.git
cd linguaspark-ai
```

2. **Install backend dependencies**
```bash
cd backend
pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
# Create .env file
echo GROQ_API_KEY=your_groq_api_key_here > .env
```

4. **Start the backend server**
```bash
python script.py
```
Backend will run at: http://127.0.0.1:8000

5. **Start the frontend server** (new terminal)
```bash
cd frontend
python script.py
```
Frontend will run at: http://localhost:3000

---

## 🎮 Usage

### Quick Start

1. **Open your browser** → http://localhost:3000
2. **Create an account** (Sign up)
3. **Select languages:**
   - I speak: Your native language
   - I want to learn: Target language
4. **Start chatting!** Type any message and learn

### Example Conversations

**Example 1:**
```
You: Hello, how are you?
LinguaSpark: In Spanish, that's "Hola, ¿cómo estás?"
- "Hola" = Hello
- "¿cómo estás?" = how are you?
Remember: In Spanish, questions use ¿ at the start!
```

**Example 2:**
```
You: I want to order food
LinguaSpark: En français: "Je veux commander de la nourriture"
- "Je veux" = I want
- "commander" = to order
- "la nourriture" = the food
Try saying: "Je voudrais un café" (I would like a coffee)
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `backend` folder:

```env
# Required
GROQ_API_KEY=your_groq_api_key_here

# Optional (for future features)
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

### Get Your Groq API Key

1. Visit https://console.groq.com
2. Sign up for free (no credit card required)
3. Navigate to API Keys
4. Create a new key
5. Copy and paste into `.env` file

---

## 📁 Project Structure

```
linguaspark-ai/
├── backend/
│   ├── .env                 # Environment variables
│   ├── main.py              # FastAPI application
│   ├── auth.py              # Authentication logic
│   ├── script.py            # Server startup
│   ├── requirements.txt     # Python dependencies
│   └── users.json           # User database
│
├── frontend/
│   ├── index.html           # Main HTML file
│   ├── app.js               # JavaScript logic
│   ├── style.css            # Styling
│   └── script.py            # Frontend server
│
├── README.md                # This file
└── TECH_STACK_ANALYSIS.md   # Tech stack details
```

---

## 🛠️ API Endpoints

### Authentication
- `POST /signup` - Create new user account
- `POST /login` - User login

### Chat
- `POST /chat` - Send message and get AI response

### Utility
- `GET /` - API information
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation
- `GET /history/{username}` - Get chat history

---

## 🧪 Testing

### Test Login System
```bash
cd backend
python test_login.py
```

### Test API Endpoints
Visit http://127.0.0.1:8000/docs for interactive API testing

### Manual Testing
1. Create account: username `testuser`, password `test123`
2. Login with credentials
3. Send message: "Hello"
4. Verify AI response

---

## 🚀 Deployment

### Frontend (Vercel)
```bash
cd frontend
vercel deploy
```

### Backend (Railway)
```bash
cd backend
railway init
railway up
```

### Environment Setup
Set these environment variables in your deployment platform:
- `GROQ_API_KEY`
- `ALLOWED_ORIGINS` (for CORS)

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 Roadmap

### v1.0 (Current)
- [x] Basic chat interface
- [x] User authentication
- [x] 10+ language support
- [x] Chat history storage
- [x] Responsive design

### v2.0 (Planned)
- [ ] Voice input/output
- [ ] Progress tracking
- [ ] Vocabulary cards
- [ ] Spaced repetition
- [ ] User profiles

### v3.0 (Future)
- [ ] Mobile apps (iOS/Android)
- [ ] Group learning rooms
- [ ] Gamification
- [ ] Certificate system
- [ ] Video lessons

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Groq** - For providing free, fast AI inference
- **FastAPI** - For the amazing Python framework
- **Llama 3.3** - For the powerful language model
- **Community** - For feedback and contributions

---

## 📧 Contact

- **Project:** LinguaSpark AI
- **Website:** [Coming Soon]
- **Email:** support@linguaspark.ai
- **Twitter:** @LinguaSparkAI

---

## ⭐ Support

If you find this project helpful:
- Give it a ⭐ on GitHub
- Share it with friends
- Report bugs
- Suggest features

---

**Made with ❤️ for language learners worldwide**

🌟 Happy Learning! 🌟
