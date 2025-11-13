"""
Configuration file for job scraper
Supports both local config and environment variables (for cloud deployment)

Copy this file to config.py and fill in your actual credentials
"""

import os

# Email Configuration
# Can be set via environment variables (for cloud) or directly here (for local)
EMAIL_CONFIG = {
    'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
    'smtp_port': int(os.getenv('SMTP_PORT', '587')),
    'sender_email': os.getenv('SENDER_EMAIL', 'your_email@gmail.com'),
    'sender_password': os.getenv('SENDER_PASSWORD', 'your_app_password_here'),
    'recipient_email': os.getenv('RECIPIENT_EMAIL', 'your_email@gmail.com'),
}

# Job Search Keywords
JOB_KEYWORDS = [
    'new grad',
    'fresher',
    'entry level',
    'internship',
    'trainee',
    'graduate',
    'junior',
    'associate'
]

# Scraping Configuration
SCRAPING_CONFIG = {
    'check_interval_minutes': int(os.getenv('CHECK_INTERVAL_MINUTES', '30')),
    'scrapers': {
        'linkedin': True,
        'internshala': True,
        'naukri': True,
        'indeed': True
    }
}

# Filter Configuration
FILTER_CONFIG = {
    'min_jobs_for_email': int(os.getenv('MIN_JOBS_FOR_EMAIL', '1')),
    'exclude_keywords': [
        'senior',
        'lead',
        'manager',
        'director',
        'vp',
        '5+ years',
        '10+ years'
    ]
}

