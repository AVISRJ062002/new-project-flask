# 🚀 DevOps CI/CD Pipeline Application

A **production-ready** Flask application with complete CI/CD pipeline using Docker, Jenkins, and Docker Hub.

![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.9-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.2-lightblue) ![Webhook](https://img.shields.io/badge/Webhook-Trigger%20Configured-yellowgreen)
![Docker](https://img.shields.io/badge/Docker-Latest-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

🎨 **Modern UI**
- Gradient background design
- Responsive grid layout
- Interactive buttons with hover effects
- Smooth animations and transitions
- Mobile-friendly interface

🐳 **Docker Integration**
- Optimized Dockerfile
- Multi-stage build support
- Health checks
- Port 5000 exposed
- Production-ready base image

⚙️ **CI/CD Pipeline**
- 7-stage Jenkins pipeline
- Automated build and push
- Docker Hub integration
- Health verification
- Error handling and logging

🚀 **Deployment Ready**
- Environment variable support
- Container orchestration
- Scalable architecture
- Production best practices

---

## 📋 Prerequisites

### Required
- **Docker** (latest)
  - Download: https://www.docker.com/products/docker-desktop
  
- **Python 3.9+** (for local testing)
  - Download: https://www.python.org/downloads/

### Optional (for full CI/CD)
- **Jenkins** (for automated pipeline)
- **Git** (for version control)
- **Docker Hub Account** (for image registry)

---

## 🚀 Quick Start

### 1️⃣ **Local Testing (Without Docker)**

```bash
# Navigate to app directory
cd app

# Install dependencies
pip install -r requirements.txt

# Run Flask app
python app.py

# Open browser
# http://localhost:5000
```

### 2️⃣ **Docker Build & Run**

```bash
# Build image
cd app
docker build -t cicd-app:latest .

# Run container
docker run -d --name cicd-app-container -p 5000:5000 cicd-app:latest

# Test the app
curl http://localhost:5000

# Stop container
docker stop cicd-app-container
docker rm cicd-app-container
```

### 3️⃣ **Docker Compose (Recommended)**

```bash
# Build and start
cd app
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## 📁 Project Structure

```
app/
├── app.py                    # Flask application (10 lines)
├── requirements.txt          # Dependencies
├── Dockerfile               # Container configuration
├── docker-compose.yml       # Docker Compose setup
├── .dockerignore            # Docker build exclusions
├── Jenkinsfile              # CI/CD pipeline
├── SETUP_GUIDE.md           # Detailed setup instructions
├── README.md                # This file
├── templates/
│   └── index.html          # Modern HTML UI
└── static/
    └── style.css           # Professional styling (350+ lines)
```

---

## 📋 Application Details

### Flask App
- **Host:** 0.0.0.0
- **Port:** 5000
- **Route:** / (renders index.html)
- **Dependencies:** Flask 2.3.2, Werkzeug 2.3.6

### Docker Image
- **Base Image:** python:3.9-slim
- **Size:** ~150MB
- **Exposed Port:** 5000
- **Health Check:** Enabled
- **Restart Policy:** Always

### Jenkinsfile Stages
1. Checkout Source
2. Build Docker Image
3. Login to Docker Hub
4. Push Docker Image
5. Deploy Container
6. Health Check
7. Cleanup

---

## 🐳 Docker Commands

### Build
```bash
# Build with tag
docker build -t cicd-app:latest .

# Build with specific version
docker build -t cicd-app:1.0 .

# Build without cache
docker build --no-cache -t cicd-app:latest .
```

### Run
```bash
# Run in background
docker run -d --name cicd-app-container -p 5000:5000 cicd-app:latest

# Run with environment variables
docker run -d -e FLASK_ENV=production -p 5000:5000 cicd-app:latest

# Run with volume mount
docker run -d -v $(pwd):/app -p 5000:5000 cicd-app:latest
```

### Debug
```bash
# View logs
docker logs cicd-app-container

# Follow logs
docker logs -f cicd-app-container

# Inspect container
docker inspect cicd-app-container

# Execute command in container
docker exec -it cicd-app-container bash
```

### Cleanup
```bash
# Stop container
docker stop cicd-app-container

# Remove container
docker rm cicd-app-container

# Remove image
docker rmi cicd-app:latest

# Remove unused resources
docker system prune
```

---

## 📤 Push to Docker Hub

### Step 1: Login
```bash
docker login
# Enter credentials when prompted
```

### Step 2: Tag Image
```bash
# Replace YOUR_USERNAME with Docker Hub username
docker tag cicd-app:latest YOUR_USERNAME/cicd-app:latest
docker tag cicd-app:latest YOUR_USERNAME/cicd-app:1.0
```

### Step 3: Push
```bash
docker push YOUR_USERNAME/cicd-app:latest
docker push YOUR_USERNAME/cicd-app:1.0
```

### Step 4: Verify
Visit: `https://hub.docker.com/r/YOUR_USERNAME/cicd-app`

---

## ⚙️ Jenkins Pipeline Setup

### Prerequisites
- Jenkins server installed and running
- Docker installed on Jenkins agent
- Pipeline plugin installed
- Git plugin installed
- GitHub plugin installed for `githubPush()` webhook triggers

### Create Credentials

**1. Docker Hub Credentials**
- Type: Username with password
- Credential ID: `docker_credentials`
- Username: Docker Hub username
- Password: Docker Hub password

**2. Docker Username**
- Type: Secret text
- Credential ID: `docker_username`
- Secret: Your Docker Hub username

**3. GitHub Repository URL**
- Type: Secret text
- Credential ID: `github_repo_url`
- Secret: https://github.com/YOUR_USERNAME/cicd-app.git

### Create Pipeline Job

1. Jenkins Dashboard → New Item
2. Name: `cicd-app-pipeline`
3. Type: Pipeline
4. Configuration:
   - Definition: Pipeline script from SCM
   - SCM: Git
   - Repository URL: https://github.com/YOUR_USERNAME/cicd-app.git
   - Branch: main
   - Script Path: app/Jenkinsfile
5. Save and Run

---

## 🔄 GitHub Integration

### Push to GitHub

```bash
cd app

# Initialize git
git init
git add .
git commit -m "Initial CI/CD project"

# Add remote (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/cicd-app.git
git branch -M main
git push -u origin main
```

### Enable Webhooks

The Jenkins pipeline now declares `githubPush()` in `app/Jenkinsfile`, but GitHub can only trigger it if Jenkins is reachable from the public internet. `localhost` will not work for GitHub deliveries.

1. Expose Jenkins at a public URL, for example `https://jenkins.example.com`
2. Run the pipeline once manually after updating the job so Jenkins stores the trigger from the Jenkinsfile
3. GitHub Repository → Settings → Webhooks
4. Add Webhook:
   - Payload URL: `https://jenkins.example.com/github-webhook/`
   - Content type: application/json
   - Events: Just the push event
   - Active: ✓
5. Push a new commit and confirm Jenkins starts automatically

---

## 🧪 Testing & Validation

### 1. Python Syntax Check
```bash
python -m py_compile app.py
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Local Flask Test
```bash
python app.py
# Visit http://localhost:5000
```

### 4. Docker Build Test
```bash
docker build -t cicd-app:latest .
```

### 5. Container Runtime Test
```bash
docker run -d --name test-app -p 5000:5000 cicd-app:latest
curl http://localhost:5000
docker logs test-app
docker stop test-app && docker rm test-app
```

### 6. Docker Hub Push Test
```bash
docker tag cicd-app:latest YOUR_USERNAME/cicd-app:test
docker push YOUR_USERNAME/cicd-app:test
```

---

## 📊 UI Features

### Components
- **Navigation Bar:** Logo and version badge
- **Hero Section:** Main heading and subtitle
- **Card Grid:** 3 feature cards (Docker, Jenkins, Docker Hub)
- **Action Buttons:** Test Pipeline and Check Status
- **Status Message:** Real-time feedback area
- **Stats Grid:** System health indicators
- **Footer:** Copyright and tech stack info

### Interactions
- Button hover effects with ripple animation
- Status message fade-in/out transitions
- Card hover with scale and shadow effects
- Smooth scroll animations
- Responsive design for all screen sizes

### Colors
- Primary Gradient: `#667eea` to `#764ba2` to `#f093fb`
- Text: `#333` (dark)
- Accents: White backgrounds with shadows
- Success: `#27ae60` (green)

---

## 🔍 Troubleshooting

### Docker daemon not running
```bash
# Start Docker Desktop
# Windows: Press Win + R, enter "docker", launch Docker Desktop
```

### Port 5000 in use
```bash
# Find process
netstat -ano | findstr :5000

# Kill process (Windows)
taskkill /PID <PID> /F

# Kill process (Linux/Mac)
lsof -ti:5000 | xargs kill -9
```

### Container won't start
```bash
# Check logs
docker logs container_name

# Inspect
docker inspect container_name

# Rebuild without cache
docker build --no-cache -t cicd-app:latest .
```

### Flask import errors
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Jenkins pipeline fails
```bash
# Check Jenkins logs
tail -f /var/log/jenkins/jenkins.log

# Verify Docker in Jenkins
docker version
docker ps

# Test credentials
docker login
```

---

## 📈 Performance Optimizations

✅ Multi-layer Docker caching
✅ Lightweight base image (python:3.9-slim)
✅ Dependency caching in Dockerfile
✅ Health checks enabled
✅ Environment variable optimization
✅ CSS/JS minification ready
✅ CDN-ready static files

---

## 🔐 Security Best Practices

✅ No hardcoded secrets
✅ Credentials in Jenkins/environment
✅ Non-root user support (ready for enhancement)
✅ Health checks enabled
✅ Image scanning ready
✅ Network isolation (Docker Compose)
✅ HTTPS support (reverse proxy ready)

---

## 📚 Useful Links

- **Flask:** https://flask.palletsprojects.com/
- **Docker:** https://docs.docker.com/
- **Jenkins:** https://www.jenkins.io/doc/
- **Docker Hub:** https://hub.docker.com/
- **GitHub:** https://github.com/

---

## 🤝 Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add improvement'`)
4. Push to branch (`git push origin feature/improvement`)
5. Create Pull Request

---

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 📞 Support

For issues and questions:
1. Check SETUP_GUIDE.md for detailed instructions
2. Review troubleshooting section above
3. Check Docker/Jenkins logs
4. Open GitHub issue with details

---

## 🎯 Next Steps

1. ✅ Setup local environment
2. ✅ Test Docker build and run
3. ✅ Push to Docker Hub
4. ✅ Setup Jenkins pipeline
5. ✅ Configure GitHub webhooks
6. ✅ Monitor deployments
7. ✅ Scale infrastructure

---

## ✅ Completion Checklist

- ✅ Flask application created and tested
- ✅ Modern responsive UI designed
- ✅ Docker containerization configured
- ✅ Jenkinsfile CI/CD pipeline created
- ✅ Docker Compose setup included
- ✅ Docker Hub integration ready
- ✅ Health checks implemented
- ✅ Documentation complete
- ✅ Production-ready code
- ✅ Error handling implemented

---

**Status:** Production Ready 🚀

**Last Updated:** May 4, 2026

**Version:** 1.0

---

Made with ❤️ by DevOps Engineering Team
