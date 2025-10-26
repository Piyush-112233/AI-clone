# 🚀 Deployment Guide - LinguaSpark AI

## Quick Deployment Options

### Option 1: Vercel + Railway (Recommended - FREE)

#### Deploy Frontend to Vercel

1. **Install Vercel CLI**
```bash
npm install -g vercel
```

2. **Create `vercel.json` in frontend folder**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "*.html",
      "use": "@vercel/static"
    }
  ]
}
```

3. **Deploy**
```bash
cd frontend
vercel
```

4. **Update API URL in `app.js`**
```javascript
const API_URL = 'https://your-backend.railway.app';
```

#### Deploy Backend to Railway

1. **Create `runtime.txt` in backend folder**
```
python-3.10
```

2. **Create `Procfile` in backend folder**
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

3. **Sign up at** https://railway.app

4. **Create new project**
- Choose "Deploy from GitHub repo"
- Or use Railway CLI: `railway login && railway init && railway up`

5. **Set environment variables**
```
GROQ_API_KEY=your_groq_api_key
```

6. **Deploy!**

---

### Option 2: Render (All-in-one - FREE)

#### Deploy Backend

1. **Create `render.yaml`**
```yaml
services:
  - type: web
    name: linguaspark-backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: GROQ_API_KEY
        sync: false
```

2. **Push to GitHub**

3. **Connect to Render** at https://render.com

#### Deploy Frontend

1. **Create `build.sh`**
```bash
#!/bin/bash
# No build needed for static site
echo "Frontend ready!"
```

2. **Deploy as Static Site** on Render

---

### Option 3: Docker (Self-hosted)

#### Create `backend/Dockerfile`
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Create `frontend/Dockerfile`
```dockerfile
FROM python:3.10-alpine

WORKDIR /app

COPY . .

EXPOSE 3000

CMD ["python", "script.py"]
```

#### Create `docker-compose.yml` in root
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
    volumes:
      - ./backend/users.json:/app/users.json
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    restart: unless-stopped
```

#### Run with Docker
```bash
docker-compose up -d
```

---

## Environment Variables Setup

### Development (.env)
```env
GROQ_API_KEY=gsk_your_dev_key
DEBUG=True
ALLOWED_ORIGINS=http://localhost:3000
```

### Production
```env
GROQ_API_KEY=gsk_your_prod_key
DEBUG=False
ALLOWED_ORIGINS=https://your-frontend-domain.com
```

---

## Pre-Deployment Checklist

- [ ] Test locally (both backend and frontend)
- [ ] Set up Git repository
- [ ] Create `.gitignore` file
- [ ] Add environment variables
- [ ] Update CORS origins in `main.py`
- [ ] Test API endpoints
- [ ] Update API_URL in frontend
- [ ] Secure sensitive data
- [ ] Add SSL certificate
- [ ] Set up custom domain (optional)

---

## Post-Deployment Tasks

1. **Test live website**
   - Create account
   - Login
   - Send messages
   - Check chat history

2. **Monitor logs**
   ```bash
   # Railway
   railway logs
   
   # Render
   # Check dashboard
   
   # Docker
   docker-compose logs -f
   ```

3. **Set up analytics** (optional)
   - Google Analytics
   - Plausible
   - Umami

4. **Set up error monitoring** (optional)
   - Sentry
   - LogRocket
   - Rollbar

---

## Custom Domain Setup

### Vercel
1. Go to project settings
2. Add custom domain
3. Update DNS records
4. SSL auto-configured

### Railway
1. Go to service settings
2. Add custom domain
3. Update CNAME record
4. SSL auto-configured

---

## Scaling & Optimization

### Backend Optimizations
```python
# Add caching
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

@app.on_event("startup")
async def startup():
    redis = await aioredis.create_redis_pool("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="linguaspark")

# Add rate limiting
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
```

### Frontend Optimizations
- Minify CSS/JS
- Enable gzip compression
- Use CDN for static assets
- Implement lazy loading
- Add service worker for offline support

---

## Troubleshooting

### Issue: CORS Error
**Solution:** Update `main.py`
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue: API Key Not Working
**Solution:** Check environment variables
```bash
# Railway
railway variables

# Render
# Check dashboard > Environment

# Vercel
vercel env ls
```

### Issue: Database Not Persisting
**Solution:** Use proper database
- Migrate to Supabase
- Use MongoDB Atlas
- Use PostgreSQL on Railway/Render

---

## Cost Breakdown

### FREE Tier (Recommended for MVP)
- **Vercel:** FREE (100GB bandwidth/month)
- **Railway:** FREE ($5 credit/month)
- **Groq API:** FREE (limited requests)
- **Total:** $0/month ✅

### Paid Tier (For Production)
- **Vercel Pro:** $20/month
- **Railway Pro:** $5-20/month
- **Supabase Pro:** $25/month
- **Custom Domain:** $10-15/year
- **Total:** ~$50/month

---

## Security Best Practices

1. **Never commit `.env` files**
2. **Use environment variables** for all secrets
3. **Enable HTTPS** (SSL)
4. **Add rate limiting**
5. **Implement JWT** for auth
6. **Sanitize user inputs**
7. **Use CORS properly**
8. **Keep dependencies updated**

---

## Monitoring & Maintenance

### Health Checks
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0"
    }
```

### Uptime Monitoring
- UptimeRobot (FREE)
- Better Uptime
- Pingdom

### Backup Strategy
```bash
# Backup users.json daily
0 0 * * * cp /app/users.json /backup/users_$(date +\%Y\%m\%d).json
```

---

## 🎉 You're Ready to Deploy!

**Recommended Path for Beginners:**
1. Push code to GitHub
2. Deploy backend to Railway
3. Deploy frontend to Vercel
4. Test everything
5. Share with the world! 🚀

**Questions?** Check the main README.md or create an issue on GitHub.
