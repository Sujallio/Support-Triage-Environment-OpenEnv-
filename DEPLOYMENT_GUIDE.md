# HuggingFace Spaces Deployment Guide

## Your Details
- **HF Username:** Sujall07
- **GitHub Repo:** https://github.com/Sujallio/Support-Triage-Environment-OpenEnv-
- **Space Repo ID:** will be `Sujall07/support-triage-env` (auto-created)
- **HF Token:** Keep secure - never hardcode in files!

## Step 1: Create HF Space (Manual - Web UI)

### 1a. Go to HuggingFace Spaces
- Visit: https://huggingface.co/spaces
- Click: "Create new Space"

### 1b. Configure Space Settings
- **Space name:** `support-triage-env` (this becomes your Space ID)
- **License:** MIT (same as your repo)
- **Space SDK:** Docker (important for Dockerfile deployment)
- **Visibility:** Public (for hackathon submission)
- Click: "Create Space"

### 1c. After Space is Created
You'll get a Space URL like:
```
https://huggingface.co/spaces/Sujall07/support-triage-env
```

## Step 2: Deploy from GitHub

### 2a. Connect GitHub Repository
In your Space settings, configure Docker deployment:
1. Go to Space Settings → "Repo details"
2. Link your GitHub repository:
   - Repo: `Sujallio/Support-Triage-Environment-OpenEnv-`
   - Branch: `main`
3. Save

### 2b. Configure Docker Build
The Dockerfile is already in your repo, so HF Spaces will auto-detect it:
- Automatically reads `Dockerfile` from repo root
- Builds Docker image
- Deploys container
- Maps port 8000 (your FastAPI app)

### 2c: Wait for Deployment
- Spaces will build your Docker image (5-10 minutes first time)
- Once built, API will be live at Space URL
- You can monitor build logs in Space settings

## Step 3: Test Your Deployed Space

### 3a. Get Space API URL
Once deployed, your Space API will be at:
```
https://Sujall07-support-triage-env.hf.space/
```

### 3b. Test /reset Endpoint
```bash
curl -X GET "https://Sujall07-support-triage-env.hf.space/reset"
```

Should return a JSON observation object.

### 3c. Test /step Endpoint
```bash
curl -X POST "https://Sujall07-support-triage-env.hf.space/step" \
  -H "Content-Type: application/json" \
  -d '{"action_type": "classify", "value": "high"}'
```

Should return reward, done status, and new observation.

### 3d. Interactive Docs
Visit Swagger UI:
```
https://Sujall07-support-triage-env.hf.space/docs
```

## Step 4: Register with OpenEnv

### 4a. Install OpenEnv CLI
```bash
pip install openenv-core
```

### 4b. Authenticate with Your Token
```bash
openenv login --token $HF_TOKEN
```
(Where $HF_TOKEN is your HuggingFace token from settings)

### 4c. Push Your Environment
```bash
openenv push --repo-id Sujall07/support-triage-env
```

This will:
- Register your environment on the OpenEnv platform
- Link your HF Space as the deployment
- Make it discoverable in the OpenEnv ecosystem

## Step 5: Final Submission

### 5a. Get Your Submission URL
Your final submission URL should be:
```
https://Sujall07-support-triage-env.hf.space/
```

OR if using openenv ecosystem:
```
Sujall07/support-triage-env
```

### 5b. Submit to Hackathon
- Go to the hackathon submission form
- Paste your HF Space URL
- Include your Space name: `Sujall07/support-triage-env`
- Verify API responds to /reset and /step

## Troubleshooting

### Space Build Fails
- Check Dockerfile syntax
- Ensure all dependencies in requirements.txt match pinned versions
- Check build logs in Space settings

### API Returns 404
- Wait 2-3 minutes after build completes for cold start
- Verify Space is in "Running" status
- Check Space environment variables if needed

### Port Issues
- Ensure Dockerfile exposes port 8000
- FastAPI must bind to 0.0.0.0 (not 127.0.0.1)
- Current app.py is correctly configured

## Quick Reference

| Step | Action | Time |
|------|--------|------|
| 1 | Create HF Space (web UI) | 2 min |
| 2 | Link GitHub repo | 1 min |
| 3 | Wait for Docker build | 5-10 min |
| 4 | Test API endpoints | 2 min |
| 5 | Register with openenv push | 2 min |
| 6 | Submit to hackathon | 1 min |
| **Total** | | **13-19 min** |

## Support

If you encounter issues:
1. Check Space logs: https://huggingface.co/spaces/Sujall07/support-triage-env
2. Verify Dockerfile is valid
3. Ensure GitHub repo is public
4. Check HF token has write permissions
