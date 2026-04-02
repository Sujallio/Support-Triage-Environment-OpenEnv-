# HuggingFace Spaces Quick Setup Checklist

## Your Account Info
- **Username:** Sujall07
- **Token:** Keep secure - set as env variable, never commit to GitHub!
- **GitHub Repo:** Sujallio/Support-Triage-Environment-OpenEnv-

---

## STEP 1: Create HF Space (Manual - 2 minutes)

- [ ] Go to https://huggingface.co/spaces
- [ ] Click "Create new Space" button
- [ ] Fill in form:
  - **Space name:** `support-triage-env`
  - **License:** MIT
  - **Space SDK:** Docker (very important!)
  - **Visibility:** Public
- [ ] Click "Create Space"
- [ ] You'll be redirected to: `https://huggingface.co/spaces/Sujall07/support-triage-env`

---

## STEP 2: Link GitHub Repository (Manual - 1 minute)

- [ ] In your new Space, go to Settings (gear icon)
- [ ] Look for "Repository details" or "Configuration"
- [ ] Enable Docker deployment
- [ ] Link GitHub repository:
  - Repository URL: `Sujallio/Support-Triage-Environment-OpenEnv-`
  - Branch: `main`
  - Linked Dockerfile: `/Dockerfile` (should auto-detect)
- [ ] Save settings

---

## STEP 3: Wait for Docker Build (5-10 minutes)

- [ ] Space will automatically start building Docker image
- [ ] You can watch the build logs in the Space
- [ ] Wait until you see: "Build successful" or "Status: Running"
- [ ] Once running, your Space API will be live at:
  ```
  https://Sujall07-support-triage-env.hf.space
  ```

---

## STEP 4: Test Your Space (2 minutes)

**Option A: Using Browser**
- [ ] Visit: `https://Sujall07-support-triage-env.hf.space/docs`
- [ ] You should see FastAPI Swagger UI
- [ ] Test `/reset` endpoint
- [ ] Test `/step` endpoint with:
  ```json
  {"action_type": "classify", "value": "high"}
  ```

**Option B: Using Terminal**
```bash
# Test reset
curl -X GET "https://Sujall07-support-triage-env.hf.space/reset"

# Test step
curl -X POST "https://Sujall07-support-triage-env.hf.space/step" \
  -H "Content-Type: application/json" \
  -d '{"action_type": "classify", "value": "high"}'
```

---

## STEP 5: Register with OpenEnv (2 minutes) - Optional

```bash
# Install CLI
pip install openenv-core

# Authenticate (set HF_TOKEN environment variable first)
openenv login --token $HF_TOKEN

# Register environment
openenv push --repo-id Sujall07/support-triage-env
```

---

## STEP 6: Submit to Hackathon (1 minute)

- [ ] Go to hackathon submission form
- [ ] Paste this URL:
  ```
  https://Sujall07-support-triage-env.hf.space
  ```
- [ ] Include environment name: `Sujall07/support-triage-env`
- [ ] Submit before deadline

---

## Final Submission URL

```
https://Sujall07-support-triage-env.hf.space
```

---

## Troubleshooting

### Issue: Space build fails
**Solution:**
- Check Space logs at: https://huggingface.co/spaces/Sujall07/support-triage-env/logs
- Verify Dockerfile syntax (we fixed it to use uvicorn)
- Ensureall dependencies in `requirements.txt` are pinned

### Issue: API returns 404
**Solution:**
- Wait 2-3 minutes after build completes (cold start)
- Check Space status is "Running" (not "Building")
- Visit `/docs` endpoint to verify FastAPI is responding

### Issue: Can't connect to Space
**Solution:**
- Space might still be building - check logs
- Verify Space visibility is "Public"
- Try accessing directly: `https://Sujall07-support-triage-env.hf.space/`

---

## What We Just Fixed

✓ Updated Dockerfile to use uvicorn (proper FastAPI server)
✓ Changed to port 7860 (HF Spaces standard)
✓ Ensured 0.0.0.0 binding (accessible from outside)
✓ Created deployment guide
✓ Created helper script

---

## Next Action

**Run this to get started:**

```bash
python deploy_to_hf.py
```

This script will:
1. Check if Space is created and built
2. Test your Space API
3. Help register with OpenEnv (optional)
4. Confirm submission details

---

Once the Space is live, your submission URL will be ready!
