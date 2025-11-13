# 🚀 Job Scraper & Email Notification System

An AI-powered tool that automatically scrapes new grad job listings and internships in India and emails you the moment they're posted, giving you a competitive edge by being one of the first to apply!

## Features

- ✅ **Multi-Source Scraping**: Scrapes from LinkedIn, Internshala, Naukri, and Indeed
- ✅ **Real-Time Notifications**: Instant email alerts when new jobs are posted
- ✅ **Smart Filtering**: Filters out senior positions, focuses on new grad/internship roles
- ✅ **Duplicate Prevention**: Tracks seen jobs to avoid duplicate notifications
- ✅ **Beautiful Email Format**: HTML emails with clickable job links
- ✅ **Configurable**: Easy to customize keywords, intervals, and filters

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Email Settings

Edit `config.py` and update the following:

```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'your_email@gmail.com',
    'sender_password': 'your_app_password_here',  # See below
    'recipient_email': 'your_email@gmail.com',
}
```

#### For Gmail Users:

1. Enable 2-Factor Authentication on your Google account
2. Generate an "App Password":
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (Custom name)"
   - Enter "Job Scraper" as the name
   - Copy the generated 16-character password
   - Use this password in `config.py` (not your regular Gmail password)

#### For Other Email Providers:

- **Outlook/Hotmail**: `smtp-mail.outlook.com`, port 587
- **Yahoo**: `smtp.mail.yahoo.com`, port 587
- **Custom SMTP**: Update `smtp_server` and `smtp_port` accordingly

### 3. Customize Job Keywords (Optional)

Edit `config.py` to add/remove keywords:

```python
JOB_KEYWORDS = [
    'new grad',
    'fresher',
    'entry level',
    'internship',
    # Add your own keywords here
]
```

### 4. Test Email Configuration

Before running the full scraper, test your email setup:

```bash
python main.py --test-email
```

You should receive a test email. If not, check your configuration.

### 5. Run the Scraper

Start the continuous monitoring:

```bash
python main.py
```

The scraper will:
- Run an initial check immediately
- Then check every 30 minutes (configurable in `config.py`)
- Send email notifications when new jobs are found
- Log all activity to `job_scraper.log`

## Configuration Options

### Scraping Interval

Change how often to check for new jobs (in `config.py`):

```python
SCRAPING_CONFIG = {
    'check_interval_minutes': 30,  # Check every 30 minutes
}
```

### Minimum Jobs for Email

Control when emails are sent:

```python
FILTER_CONFIG = {
    'min_jobs_for_email': 1,  # Send email even for 1 new job
}
```

### Exclude Keywords

Filter out unwanted job types:

```python
FILTER_CONFIG = {
    'exclude_keywords': [
        'senior',
        'lead',
        'manager',
        # Add keywords to exclude
    ]
}
```

## Running in Background

### Windows (Task Scheduler)

1. Create a batch file `run_scraper.bat`:
```batch
@echo off
cd /d "C:\path\to\your\project"
python main.py
```

2. Use Task Scheduler to run it at startup or on a schedule

### Linux/Mac (Cron or systemd)

Add to crontab for continuous running:
```bash
crontab -e
# Add this line (runs every 30 minutes):
*/30 * * * * cd /path/to/project && /usr/bin/python3 main.py
```

Or use `nohup` to run in background:
```bash
nohup python main.py > scraper.log 2>&1 &
```

## Database

The scraper uses SQLite database (`jobs.db`) to track:
- All scraped jobs
- Which jobs have been notified
- Prevents duplicate notifications

You can delete `jobs.db` to reset the tracking (will resend all jobs).

## Troubleshooting

### Email Not Sending

1. **Check App Password**: Make sure you're using an App Password, not your regular password
2. **Check SMTP Settings**: Verify `smtp_server` and `smtp_port` are correct
3. **Test Email First**: Run `python main.py --test-email` to isolate email issues
4. **Check Firewall**: Ensure port 587 is not blocked

### No Jobs Found

1. **Check Internet Connection**: Scraper needs internet access
2. **Website Changes**: Job sites may have changed their HTML structure
3. **Rate Limiting**: Some sites may temporarily block requests (wait and retry)
4. **Check Logs**: Review `job_scraper.log` for detailed error messages

### Scraper Stops Working

1. **Check Logs**: `job_scraper.log` contains detailed error information
2. **Website Structure Changed**: Job sites update their HTML - scrapers may need updates
3. **Network Issues**: Check your internet connection

## Legal & Ethical Considerations

- ✅ This tool is for personal use only
- ✅ Respects robots.txt and rate limits
- ✅ Uses reasonable delays between requests
- ⚠️ Some job sites may have terms of service restrictions
- ⚠️ Use responsibly and don't overload servers

## Future Enhancements

Potential improvements:
- [ ] Add more job sites (Glassdoor, Monster, etc.)
- [ ] Machine learning for better job matching
- [ ] Resume auto-application (if sites allow)
- [ ] Web dashboard for viewing jobs
- [ ] SMS notifications via Twilio
- [ ] Telegram bot integration

## License

This project is for personal use. Use responsibly and in accordance with job site terms of service.

## Support

If you encounter issues:
1. Check the logs in `job_scraper.log`
2. Verify your configuration in `config.py`
3. Test email separately with `--test-email` flag

---

**Good luck with your job search! 🎯**

