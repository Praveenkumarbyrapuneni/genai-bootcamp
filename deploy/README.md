# 🚀 CareerPath AI - Azure Deployment Guide

## ⚡ ONE COMMAND DEPLOYMENT (Recommended)

**Tomorrow, just run this single command:**

```bash
cd "/Users/praveen/Desktop/careerpath with auth"
./deploy/deploy-container-apps.sh
```

This will automatically:
1. ✅ Create Azure Container Registry
2. ✅ Build & push Docker image
3. ✅ Create Container Apps environment
4. ✅ Deploy FastAPI backend with all environment variables
5. ✅ Build & deploy Next.js frontend
6. ✅ Give you live URLs

---

## 📋 Prerequisites (Do This Today)

### 1. Install Docker Desktop
Download and install from: https://www.docker.com/products/docker-desktop/

**Make sure Docker is running** (whale icon in menu bar)

### 2. Verify Azure CLI is logged in
```bash
az account show
```

### 3. Verify your .env file has all credentials
Your `.env` file should have:
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_DEPLOYMENT_NAME`
- `COSMOS_CONNECTION_STRING`
- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`

---

## 🎯 What Gets Deployed

| Component | Azure Service | Cost |
|-----------|---------------|------|
| **Backend API** | Azure Container Apps | Free tier (180k vCPU-sec/month) |
| **Container Registry** | Azure Container Registry | ~$5/month (Basic) |
| **Frontend** | Azure Static Web Apps | Free |

**Total estimated cost: ~$5-10/month**

---

## 🔧 After Deployment

### 1. Test the API
```bash
curl https://careerpath-api.<random>.azurecontainerapps.io/health
```

### 2. Update Supabase Redirect URLs
Go to **Supabase Dashboard** → **Authentication** → **URL Configuration**

Add your frontend URL:
```
https://careerpath-frontend.azurestaticapps.net
```

### 3. Visit Your App!
Open the frontend URL in your browser and login with GitHub/Google.

---

## 📁 Deployment Files

| File | Purpose |
|------|---------|
| `Dockerfile` | Containerizes the FastAPI backend |
| `.dockerignore` | Excludes unnecessary files from Docker build |
| `deploy/deploy-container-apps.sh` | **Main one-command deployment script** |
| `deploy/deployment-info.txt` | Created after deployment with your URLs |

---

## 🔄 Redeployment (After Code Changes)

If you make changes to your code, just run the same command again:

```bash
./deploy/deploy-container-apps.sh
```

It will rebuild and redeploy only what's changed.

---

## 🆘 Troubleshooting

### Docker not running?
```bash
open -a Docker
# Wait for Docker to start, then retry
```

### Azure login expired?
```bash
az login
```

### Check container logs?
```bash
az containerapp logs show --name careerpath-api --resource-group careerpath-rg --follow
```

### Delete everything and start fresh?
```bash
az group delete --name careerpath-rg --yes --no-wait
```
