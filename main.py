"""
Main script to run the job scraper and email notification system
"""

import schedule
import time
import logging
from datetime import datetime
from job_scraper import scrape_all_jobs
from database import JobDatabase
from email_notifier import EmailNotifier
from config import EMAIL_CONFIG, JOB_KEYWORDS, SCRAPING_CONFIG, FILTER_CONFIG

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('job_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def filter_jobs(jobs):
    """Filter jobs based on exclude keywords"""
    filtered = []
    exclude_keywords = [kw.lower() for kw in FILTER_CONFIG.get('exclude_keywords', [])]
    
    for job in jobs:
        title_lower = job.get('title', '').lower()
        should_exclude = any(keyword in title_lower for keyword in exclude_keywords)
        
        if not should_exclude:
            filtered.append(job)
        else:
            logger.debug(f"Excluded job: {job.get('title')} (contains exclude keyword)")
    
    return filtered


def check_and_notify():
    """Main function to check for new jobs and send notifications"""
    logger.info("=" * 60)
    logger.info("Starting job scrape check...")
    logger.info(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Initialize database
        db = JobDatabase()
        
        # Scrape jobs from all sources
        logger.info(f"Scraping jobs with keywords: {JOB_KEYWORDS}")
        all_jobs = scrape_all_jobs(JOB_KEYWORDS)
        logger.info(f"Total jobs scraped: {len(all_jobs)}")
        
        # Filter jobs
        filtered_jobs = filter_jobs(all_jobs)
        logger.info(f"Jobs after filtering: {len(filtered_jobs)}")
        
        # Add to database and get only new jobs
        new_jobs = db.add_jobs(filtered_jobs)
        logger.info(f"New jobs found: {len(new_jobs)}")
        
        # Send email if we have new jobs
        if len(new_jobs) >= FILTER_CONFIG.get('min_jobs_for_email', 1):
            logger.info("Sending email notification...")
            
            # Initialize email notifier
            notifier = EmailNotifier(
                smtp_server=EMAIL_CONFIG['smtp_server'],
                smtp_port=EMAIL_CONFIG['smtp_port'],
                email=EMAIL_CONFIG['sender_email'],
                password=EMAIL_CONFIG['sender_password']
            )
            
            # Send email
            success = notifier.send_email(
                recipient=EMAIL_CONFIG['recipient_email'],
                jobs=new_jobs
            )
            
            if success:
                # Mark jobs as notified
                unnotified = db.get_unnotified_jobs()
                for job in unnotified:
                    if any(nj['url'] == job['url'] for nj in new_jobs):
                        db.mark_as_notified(job['id'])
                logger.info("Email sent successfully!")
            else:
                logger.error("Failed to send email")
        else:
            logger.info(f"Not enough new jobs ({len(new_jobs)}) to send email (minimum: {FILTER_CONFIG.get('min_jobs_for_email', 1)})")
        
        # Print stats
        stats = db.get_stats()
        logger.info(f"Database stats - Total: {stats['total_jobs']}, Notified: {stats['notified_jobs']}, Unnotified: {stats['unnotified_jobs']}")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"Error in check_and_notify: {e}", exc_info=True)


def test_email():
    """Test email configuration"""
    logger.info("Testing email configuration...")
    
    try:
        notifier = EmailNotifier(
            smtp_server=EMAIL_CONFIG['smtp_server'],
            smtp_port=EMAIL_CONFIG['smtp_port'],
            email=EMAIL_CONFIG['sender_email'],
            password=EMAIL_CONFIG['sender_password']
        )
        
        success = notifier.send_test_email(EMAIL_CONFIG['recipient_email'])
        if success:
            logger.info("✅ Test email sent successfully! Check your inbox.")
        else:
            logger.error("❌ Failed to send test email. Check your configuration.")
    except Exception as e:
        logger.error(f"Error testing email: {e}", exc_info=True)


def main():
    """Main entry point"""
    logger.info("Job Scraper and Email Notification System")
    logger.info("=" * 60)
    
    # Validate configuration
    # Check if email is still the default placeholder (means not configured)
    if EMAIL_CONFIG['sender_email'] == 'your_email@gmail.com' or not EMAIL_CONFIG['sender_email']:
        logger.error("⚠️  Please configure your email settings in config.py or environment variables!")
        logger.error("   Update EMAIL_CONFIG with your email credentials.")
        return
    
    # Schedule job checks
    interval = SCRAPING_CONFIG.get('check_interval_minutes', 30)
    logger.info(f"Scheduling job checks every {interval} minutes...")
    
    schedule.every(interval).minutes.do(check_and_notify)
    
    # Run immediately on start
    logger.info("Running initial check...")
    check_and_notify()
    
    # Keep running
    logger.info(f"Monitoring started. Checking every {interval} minutes...")
    logger.info("Press Ctrl+C to stop.")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute if any scheduled jobs are due
    except KeyboardInterrupt:
        logger.info("\nStopping job scraper...")
        logger.info("Goodbye!")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--test-email':
        test_email()
    else:
        main()

