"""
Test script to diagnose deployment issues
Run this to test email and scraper functionality
"""

import os
import sys
import logging

# Try to import config, fallback to environment variables
try:
    from config import EMAIL_CONFIG
except ImportError:
    # Fallback for cloud deployment
    EMAIL_CONFIG = {
        'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
        'smtp_port': int(os.getenv('SMTP_PORT', '587')),
        'sender_email': os.getenv('SENDER_EMAIL', ''),
        'sender_password': os.getenv('SENDER_PASSWORD', ''),
        'recipient_email': os.getenv('RECIPIENT_EMAIL', ''),
    }

from email_notifier import EmailNotifier
from job_scraper import scrape_all_jobs
from database import JobDatabase

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_environment_variables():
    """Test if environment variables are set"""
    logger.info("=" * 60)
    logger.info("Testing Environment Variables...")
    logger.info("=" * 60)
    
    required_vars = ['SENDER_EMAIL', 'SENDER_PASSWORD', 'RECIPIENT_EMAIL']
    all_set = True
    
    for var in required_vars:
        env_value = os.getenv(var)
        config_value = EMAIL_CONFIG.get(var.lower().replace('sender_', 'sender_').replace('recipient_', 'recipient_'))
        
        if env_value:
            logger.info(f"✅ {var}: Set (from environment)")
        elif config_value and config_value != f'your_{var.lower()}@gmail.com':
            logger.info(f"✅ {var}: Set (from config.py)")
        else:
            logger.error(f"❌ {var}: NOT SET")
            all_set = False
    
    logger.info("=" * 60)
    return all_set


def test_email_config():
    """Test email configuration"""
    logger.info("=" * 60)
    logger.info("Testing Email Configuration...")
    logger.info("=" * 60)
    
    try:
        notifier = EmailNotifier(
            smtp_server=EMAIL_CONFIG['smtp_server'],
            smtp_port=EMAIL_CONFIG['smtp_port'],
            email=EMAIL_CONFIG['sender_email'],
            password=EMAIL_CONFIG['sender_password']
        )
        
        logger.info(f"SMTP Server: {EMAIL_CONFIG['smtp_server']}:{EMAIL_CONFIG['smtp_port']}")
        logger.info(f"Sender: {EMAIL_CONFIG['sender_email']}")
        logger.info(f"Recipient: {EMAIL_CONFIG['recipient_email']}")
        logger.info(f"Password: {'*' * len(EMAIL_CONFIG['sender_password'])} (hidden)")
        
        logger.info("\nSending test email...")
        success = notifier.send_test_email(EMAIL_CONFIG['recipient_email'])
        
        if success:
            logger.info("✅ Test email sent successfully!")
            logger.info("   Check your inbox (and spam folder)")
            return True
        else:
            logger.error("❌ Failed to send test email")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error testing email: {e}", exc_info=True)
        return False


def test_scrapers():
    """Test job scrapers"""
    logger.info("=" * 60)
    logger.info("Testing Job Scrapers...")
    logger.info("=" * 60)
    
    try:
        keywords = ['fresher', 'internship']
        logger.info(f"Testing with keywords: {keywords}")
        
        jobs = scrape_all_jobs(keywords)
        logger.info(f"✅ Total jobs scraped: {len(jobs)}")
        
        if jobs:
            logger.info("\nSample jobs:")
            for i, job in enumerate(jobs[:3], 1):
                logger.info(f"  {i}. {job.get('title', 'N/A')} at {job.get('company', 'Unknown')} ({job.get('source', 'Unknown')})")
        
        return len(jobs) > 0
        
    except Exception as e:
        logger.error(f"❌ Error testing scrapers: {e}", exc_info=True)
        return False


def test_database():
    """Test database functionality"""
    logger.info("=" * 60)
    logger.info("Testing Database...")
    logger.info("=" * 60)
    
    try:
        db = JobDatabase()
        stats = db.get_stats()
        
        logger.info(f"✅ Database initialized")
        logger.info(f"   Total jobs: {stats['total_jobs']}")
        logger.info(f"   Notified: {stats['notified_jobs']}")
        logger.info(f"   Unnotified: {stats['unnotified_jobs']}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error testing database: {e}", exc_info=True)
        return False


def main():
    """Run all tests"""
    logger.info("\n" + "=" * 60)
    logger.info("DEPLOYMENT DIAGNOSTIC TEST")
    logger.info("=" * 60 + "\n")
    
    results = {
        'Environment Variables': test_environment_variables(),
        'Email Configuration': test_email_config(),
        'Job Scrapers': test_scrapers(),
        'Database': test_database()
    }
    
    logger.info("\n" + "=" * 60)
    logger.info("TEST RESULTS SUMMARY")
    logger.info("=" * 60)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        logger.info(f"{test_name}: {status}")
    
    logger.info("=" * 60)
    
    if all(results.values()):
        logger.info("\n🎉 All tests passed! Your deployment should work.")
    else:
        logger.info("\n⚠️  Some tests failed. Check the errors above.")
        logger.info("   See TROUBLESHOOTING.md for solutions.")


if __name__ == "__main__":
    main()

