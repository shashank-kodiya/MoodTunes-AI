# Deployment Guide

## 🚀 Deployment Options

This guide covers deploying the Emotion-Based Music Recommendation App to various platforms.

## 1. Local Deployment (Development)

### Prerequisites
- Python 3.8+
- pip
- Webcam
- ~1GB storage

### Steps

```bash
# Clone/navigate to project
cd "/Users/raristore/mini project"

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies 
pip install -r requirements.txt

# Run app
streamlit run app.py
```


**Access**: http://localhost:8501

---

## 2. Streamlit Cloud Deployment

### Prerequisites
- GitHub account
- Streamlit Cloud account (free)

### Steps

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Visit https://share.streamlit.io
   - Click "New app"
   - Select your repository and `app.py`
   - Deploy

3. **Configure Secrets** (if needed)
   - In Streamlit Cloud, add `.streamlit/secrets.toml`
   - Store API keys, credentials, etc.

### Limitations
- ⚠️ Webcam access may be limited in cloud environment
- ⚠️ Only works with HTTPS
- ✅ Good for demonstration/preview

**Access**: https://[username]-emotion-music-app.streamlit.app

---

## 3. Docker Deployment

### Create Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose port
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and Run Docker

```bash
# Build image
docker build -t emotion-music-app:latest .

# Run container
docker run -p 8501:8501 \
  --device=/dev/video0 \
  emotion-music-app:latest
```

**Access**: http://localhost:8501

### Push to Docker Hub

```bash
# Tag image
docker tag emotion-music-app:latest username/emotion-music-app:latest

# Push
docker login
docker push username/emotion-music-app:latest
```

---

## 4. Heroku Deployment

### Create Heroku Files

**Procfile:**
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

**setup.sh:**
```bash
mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your@email.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableXsrfProtection = false\n\
" > ~/.streamlit/config.toml
```

### Deploy

```bash
# Install Heroku CLI
brew tap heroku/brew && brew install heroku

# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

**Limitation**: Webcam won't work on Heroku (headless environment)

---

## 5. AWS Deployment

### Using EC2

```bash
# Launch EC2 instance (Ubuntu 20.04)
# SSH into instance

# Install Python and dependencies
sudo apt-get update
sudo apt-get install -y python3 python3-pip

# Clone repository
git clone <your-repo>
cd mini\ project

# Install requirements
pip3 install -r requirements.txt

# Run with nohup for background execution
nohup streamlit run app.py --server.port=8501 &

# Access via: http://<ec2-ip>:8501
```

### Using AWS App Runner

1. Connect GitHub repository
2. Set configuration:
   - Runtime: Python 3
   - Build command: `pip install -r requirements.txt`
   - Start command: `streamlit run app.py --server.port=8080`
3. Deploy

---

## 6. Google Cloud Run Deployment

### Create Dockerfile (same as Docker section)

### Deploy

```bash
# Install Google Cloud SDK
# Initialize gcloud
gcloud init

# Build and push to Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/emotion-music-app

# Deploy to Cloud Run
gcloud run deploy emotion-music-app \
  --image gcr.io/PROJECT_ID/emotion-music-app \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## 7. DigitalOcean Deployment

### Using Droplet

```bash
# SSH into droplet

# Install dependencies
sudo apt-get update
sudo apt-get install -y python3 python3-pip

# Install Supervisor (for process management)
sudo apt-get install -y supervisor

# Clone and setup project
git clone <your-repo>
cd mini\ project
pip3 install -r requirements.txt

# Create Supervisor config: /etc/supervisor/conf.d/app.conf
[program:emotion-app]
command=/usr/bin/python3 /home/user/mini\ project/app.py run
directory=/home/user/mini\ project
user=user
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/emotion-app.log

# Start supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start emotion-app

# Configure Nginx as reverse proxy
# Access via your domain
```

---

## 8. Production Considerations

### Security
- [ ] Use HTTPS only
- [ ] Implement authentication
- [ ] Validate user inputs
- [ ] Add rate limiting
- [ ] Secure API keys in environment variables

### Performance
- [ ] Use caching for model predictions
- [ ] Implement request queuing
- [ ] Monitor resource usage
- [ ] Scale horizontally if needed
- [ ] Use CDN for static assets

### Reliability
- [ ] Add health checks
- [ ] Implement error logging
- [ ] Set up monitoring/alerting
- [ ] Create backup/recovery plan
- [ ] Use load balancing

### Optimization

```python
# Add caching to emotion detector
import streamlit as st

@st.cache_resource
def load_detector():
    from emotion_detector import EmotionDetector
    return EmotionDetector()

detector = load_detector()
```

---

## 9. Environment Variables

Create `.env` file:
```
FLASK_ENV=production
TENSORFLOW_CPP_MIN_LOG_LEVEL=2
PYTHONUNBUFFERED=1
PORT=8501
```

Load in app:
```python
import os
from dotenv import load_dotenv

load_dotenv()
port = os.getenv('PORT', 8501)
```

---

## 10. Health Check Endpoint

Add to `app.py`:
```python
# Health check for deployment monitoring
@st.cache_resource
def get_health_status():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }
```

---

## 11. Monitoring & Logging

### Using Python Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
logger.info("App started")
```

### Monitoring Services
- **Sentry**: Error tracking
- **DataDog**: Performance monitoring
- **New Relic**: Application monitoring
- **CloudWatch**: AWS monitoring

---

## 12. Scaling Strategies

### Horizontal Scaling
- Deploy multiple instances
- Use load balancer
- Share state via database

### Vertical Scaling
- Increase CPU/RAM
- Use GPU for faster inference
- Optimize code for efficiency

### Optimization
- Model quantization
- Request batching
- Caching strategies
- Async processing

---

## 13. Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Webcam not working in cloud | Use local deployment or pre-recorded video |
| Memory issues | Reduce model size, use quantization |
| Slow inference | Use GPU, optimize preprocessing |
| Rate limiting | Implement request queuing |
| High latency | Add caching, optimize model |

---

## 14. Cost Estimation

| Platform | Monthly Cost |
|----------|-------------|
| Local/PC | $0 |
| Streamlit Cloud | Free-$20 |
| Docker Hub | Free-$5 |
| Heroku | Free-$7+ |
| AWS EC2 | ~$5-30 |
| Google Cloud Run | ~$1-10 |
| DigitalOcean | ~$5-20 |

---

## 15. Maintenance

### Regular Tasks
- [ ] Update dependencies monthly
- [ ] Monitor error logs
- [ ] Check performance metrics
- [ ] Update model if accuracy drops
- [ ] Security patches
- [ ] Backup data regularly

### Checklist
```bash
# Weekly
- Check logs
- Monitor uptime
- Review user feedback

# Monthly
- Update dependencies: pip install --upgrade -r requirements.txt
- Test all features
- Review performance metrics

# Quarterly
- Security audit
- Performance optimization
- Feature updates
- Model retraining
```

---

## Summary

| Deployment Type | Best For | Ease | Cost |
|---|---|---|---|
| Local | Development | ⭐⭐⭐⭐⭐ | $ |
| Streamlit Cloud | Demo/Portfolio | ⭐⭐⭐⭐ | $ |
| Docker | Any platform | ⭐⭐⭐ | $-$$ |
| Heroku | Quick deployment | ⭐⭐⭐⭐ | $$ |
| AWS | Production | ⭐⭐ | $$ |
| GCP | Production | ⭐⭐ | $$ |

**Recommended for portfolio/demo**: Streamlit Cloud or DigitalOcean
**Recommended for production**: AWS, GCP, or DigitalOcean

---

For detailed deployment documentation, refer to each platform's official guides.
