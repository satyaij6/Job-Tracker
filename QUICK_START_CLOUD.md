# ⚡ Quick Start: Deploy to Railway (5 Minutes)

Get your job scraper running 24/7 in 5 minutes!

## Step 1: Push to GitHub (2 min)

1. Create a new repository on GitHub
2. Push your code:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

## Step 2: Deploy to Railway (3 min)

1. **Go to Railway**: https://railway.app
2. **Sign up** with GitHub (free)
3. **Click "New Project"** → **"Deploy from GitHub repo"**
4. **Select your repository**
5. **Add Environment Variables** (click on your project → Variables):
   ```
   SENDER_EMAIL=satyainjamuri7@gmail.com
   SENDER_PASSWORD=zesy qymg znaf gbrv
   RECIPIENT_EMAIL=satyainjamuri7@gmail.com
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   CHECK_INTERVAL_MINUTES=30
   MIN_JOBS_FOR_EMAIL=1
   ```
6. **Done!** ✅ Your scraper is now running 24/7!

## That's it! 🎉

Your job scraper will:
- ✅ Run 24/7 automatically
- ✅ Check for jobs every 30 minutes
- ✅ Email you when new jobs are found
- ✅ Work even when your laptop is off

## View Logs

- Go to Railway dashboard → Your project → Deployments → View logs
- You'll see all scraping activity in real-time

## Stop/Start

- **Stop**: Click "Pause" in Railway dashboard
- **Start**: Click "Resume" in Railway dashboard

---

**Need help?** Check `DEPLOYMENT.md` for detailed instructions and other platforms.

