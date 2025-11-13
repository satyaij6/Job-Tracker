# 🚀 24/7 Cloud Deployment Guide

To run your job scraper 24/7, you need to deploy it to a cloud service. Here are the **best FREE options**:

## Option 1: Railway (Recommended - Easiest) ⭐

**Railway** offers free tier with $5 credit monthly - perfect for this project!

### Steps:

1. **Sign up**: Go to https://railway.app and sign up with GitHub

2. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Connect your GitHub account
   - Select your repository (or create one and push this code)

3. **Set Environment Variables**:
   - Go to your project → Variables tab
   - Add these variables:
     ```
     SENDER_EMAIL=satyainjamuri7@gmail.com
     SENDER_PASSWORD=zesy qymg znaf gbrv
     RECIPIENT_EMAIL=satyainjamuri7@gmail.com
     SMTP_SERVER=smtp.gmail.com
     SMTP_PORT=587
     CHECK_INTERVAL_MINUTES=30
     MIN_JOBS_FOR_EMAIL=1
     ```

4. **Deploy**:
   - Railway will auto-detect Python
   - It will run `python main.py` automatically
   - Your scraper is now running 24/7! 🎉

**Cost**: FREE (with $5 monthly credit)

---

## Option 2: Render (Free Tier Available)

**Render** offers free tier with some limitations.

### Steps:

1. **Sign up**: Go to https://render.com and sign up

2. **Create New Web Service**:
   - Click "New +" → "Background Worker"
   - Connect your GitHub repo
   - Settings:
     - **Name**: job-scraper
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python main.py`

3. **Set Environment Variables**:
   - Go to Environment tab
   - Add the same variables as Railway (see above)

4. **Deploy**: Click "Create Background Worker"

**Note**: Free tier may sleep after inactivity, but will wake up when scheduled tasks run.

**Cost**: FREE (with limitations)

---

## Option 3: PythonAnywhere (Free Tier)

**PythonAnywhere** is great for Python scripts.

### Steps:

1. **Sign up**: Go to https://www.pythonanywhere.com (free account)

2. **Upload Files**:
   - Go to Files tab
   - Upload all your project files

3. **Set Environment Variables**:
   - Go to Tasks tab
   - Create a new task with:
     ```bash
     export SENDER_EMAIL='satyainjamuri7@gmail.com'
     export SENDER_PASSWORD='zesy qymg znaf gbrv'
     export RECIPIENT_EMAIL='satyainjamuri7@gmail.com'
     python3.10 main.py
     ```

4. **Schedule Task**:
   - Go to Tasks tab
   - Set to run "Every hour" or use cron

**Cost**: FREE (with limitations)

---

## Option 4: Google Cloud Run (Free Tier)

**Google Cloud Run** offers generous free tier.

### Steps:

1. **Install Google Cloud SDK**: https://cloud.google.com/sdk/docs/install

2. **Create Dockerfile** (I'll create this for you)

3. **Deploy**:
   ```bash
   gcloud run deploy job-scraper --source . --set-env-vars SENDER_EMAIL=...,SENDER_PASSWORD=...
   ```

**Cost**: FREE (generous free tier)

---

## Option 5: AWS Lambda + EventBridge (Free Tier)

For serverless approach (runs on schedule, not continuously).

### Steps:

1. **Package as Lambda function**
2. **Set up EventBridge** to trigger every 30 minutes
3. **Configure environment variables**

**Cost**: FREE (within free tier limits)

---

## Quick Setup: Railway (Recommended)

**Fastest way to get 24/7 running:**

1. Push your code to GitHub
2. Go to https://railway.app
3. Click "New Project" → "Deploy from GitHub"
4. Add environment variables (see above)
5. Done! ✅

Your scraper will run 24/7 automatically.

---

## Environment Variables Reference

Set these in your cloud platform:

```
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
RECIPIENT_EMAIL=your_email@gmail.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
CHECK_INTERVAL_MINUTES=30
MIN_JOBS_FOR_EMAIL=1
```

---

## Monitoring

- **Railway**: Check logs in dashboard
- **Render**: View logs in dashboard
- **PythonAnywhere**: Check Tasks tab for logs

All platforms will email you when new jobs are found!

---

## Troubleshooting

### Script stops after deployment:
- Check logs in your platform's dashboard
- Verify environment variables are set correctly
- Ensure requirements.txt is in your repo

### No emails received:
- Verify SENDER_PASSWORD is an App Password (not regular password)
- Check spam folder
- Review logs for email errors

### High costs:
- Use Railway or Render free tiers
- Reduce CHECK_INTERVAL_MINUTES if needed

---

**Recommended**: Start with **Railway** - it's the easiest and most reliable for this use case! 🚀

