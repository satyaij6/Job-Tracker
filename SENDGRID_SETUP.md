# 📧 SendGrid Setup Guide - Step by Step

Since Railway is blocking SMTP connections, let's use SendGrid API instead. It's free and reliable!

## Step 1: Sign Up for SendGrid (Free)

1. **Go to**: https://sendgrid.com
2. **Click "Start for Free"**
3. **Sign up** with your email (use the same email: satyainjamuri7@gmail.com)
4. **Verify your email** (check your inbox)

## Step 2: Create API Key

1. **After logging in**, go to **Settings** → **API Keys** (left sidebar)
2. **Click "Create API Key"** button
3. **Name it**: "Job Scraper" (or any name you like)
4. **Select permissions**: Choose **"Full Access"** (or at least "Mail Send")
5. **Click "Create & View"**
6. **IMPORTANT**: Copy the API key immediately! It will only be shown once.
   - It looks like: `SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - Copy the entire key (it's long!)

## Step 3: Verify Sender Identity (Required for Free Tier)

SendGrid requires you to verify your sender email:

1. Go to **Settings** → **Sender Authentication**
2. Click **"Verify a Single Sender"**
3. Fill in the form:
   - **From Email Address**: `satyainjamuri7@gmail.com`
   - **From Name**: Your name (e.g., "Satya")
   - **Reply To**: `satyainjamuri7@gmail.com`
   - **Company Address**: Your address
   - **City**: Your city
   - **State**: Your state
   - **Country**: India
   - **Zip Code**: Your zip code
4. **Click "Create"**
5. **Check your email** - SendGrid will send a verification email
6. **Click the verification link** in the email

## Step 4: Add Environment Variables to Railway

1. **Go to Railway**: https://railway.app
2. **Click your project** → **Variables** tab
3. **Add these new variables**:

```
USE_SENDGRID=true
SENDGRID_API_KEY=SG.your_actual_api_key_here
SENDER_EMAIL=satyainjamuri7@gmail.com
RECIPIENT_EMAIL=satyainjamuri7@gmail.com
```

**Important:**
- Replace `SG.your_actual_api_key_here` with the actual API key you copied
- Keep `USE_SENDGRID=true` (this tells the code to use SendGrid)
- You can remove or keep the SMTP variables (they won't be used)

## Step 5: Deploy

The code is already updated! Railway will automatically redeploy when you push, or you can:

1. **Go to Railway** → Your Project → **Deployments**
2. **Click "Redeploy"** (or wait for auto-deploy)

## Step 6: Test

1. **Check Railway logs** after deployment
2. **Look for**: "Using SendGrid API for email delivery..."
3. **Look for**: "✅ Email sent successfully via SendGrid..."

## Troubleshooting

### "Sender not verified" error
- Make sure you verified your sender email in SendGrid
- Check your email for the verification link

### "API key invalid" error
- Double-check the API key in Railway variables
- Make sure there are no extra spaces
- The key should start with `SG.`

### "Permission denied" error
- Make sure your API key has "Mail Send" permissions
- Create a new API key with full access

## SendGrid Free Tier Limits

- ✅ **100 emails per day** (more than enough for job notifications!)
- ✅ **Free forever** (no credit card required)
- ✅ **Reliable delivery**
- ✅ **No SMTP blocking issues**

## What Happens Now

1. ✅ Code automatically uses SendGrid if `USE_SENDGRID=true`
2. ✅ Falls back to SMTP if SendGrid fails (but SMTP is blocked, so this won't work)
3. ✅ Sends beautiful HTML emails with job listings
4. ✅ Works 24/7 on Railway

## Success!

Once set up, you'll receive emails like:
- Subject: "🎯 110 New Job Listing(s) Found!"
- Beautiful HTML format with all job details
- Clickable links to apply

Your job scraper will now work perfectly! 🚀

