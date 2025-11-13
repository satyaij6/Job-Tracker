"""
Main script to run the job scraper and email notification system
"""

import schedule
import time
import logging
import os
from datetime import datetime
from job_scraper import scrape_all_jobs
from database import JobDatabase
from email_notifier import EmailNotifier

# Initialize logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Try to import config, fallback to environment variables if not available
try:
    from config import EMAIL_CONFIG, JOB_KEYWORDS, SCRAPING_CONFIG, FILTER_CONFIG
except ImportError:
    # Fallback: Read from environment variables (for cloud deployment)
    logger.warning("config.py not found, using environment variables only")
    
    EMAIL_CONFIG = {
        'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
        'smtp_port': int(os.getenv('SMTP_PORT', '587')),
        'sender_email': os.getenv('SENDER_EMAIL', ''),
        'sender_password': os.getenv('SENDER_PASSWORD', ''),
        'recipient_email': os.getenv('RECIPIENT_EMAIL', ''),
    }
    
    # Parse JOB_KEYWORDS from environment or use defaults
    keywords_str = os.getenv('JOB_KEYWORDS', '')
    if keywords_str:
        JOB_KEYWORDS = [k.strip() for k in keywords_str.split(',')]
    else:
        JOB_KEYWORDS = [
            'new grad', 'fresher', 'entry level', 'internship',
            'trainee', 'graduate', 'junior', 'associate'
        ]
    
    SCRAPING_CONFIG = {
        'check_interval_minutes': int(os.getenv('CHECK_INTERVAL_MINUTES', '30')),
        'scrapers': {
            'linkedin': os.getenv('SCRAPER_LINKEDIN', 'true').lower() == 'true',
            'internshala': os.getenv('SCRAPER_INTERNSHALA', 'true').lower() == 'true',
            'naukri': os.getenv('SCRAPER_NAUKRI', 'true').lower() == 'true',
            'indeed': os.getenv('SCRAPER_INDEED', 'true').lower() == 'true',
        }
    }
    
    exclude_keywords_str = os.getenv('EXCLUDE_KEYWORDS', '')
    if exclude_keywords_str:
        exclude_keywords = [k.strip() for k in exclude_keywords_str.split(',')]
    else:
        exclude_keywords = ['senior', 'lead', 'manager', 'director', 'vp', '5+ years', '10+ years']
    
    FILTER_CONFIG = {
        'min_jobs_for_email': int(os.getenv('MIN_JOBS_FOR_EMAIL', '1')),
        'exclude_keywords': exclude_keywords
    }

# Add file handler if running locally (file may not be writable in cloud)
try:
    file_handler = logging.FileHandler('job_scraper.log')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)
except Exception:
    # File logging not available (e.g., in cloud environment)
    pass


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
        logger.info("Starting scraping process...")
        all_jobs = scrape_all_jobs(JOB_KEYWORDS)
        logger.info(f"✅ Scraping complete! Total jobs scraped: {len(all_jobs)}")
        
        # Filter jobs
        logger.info("Filtering jobs...")
        filtered_jobs = filter_jobs(all_jobs)
        logger.info(f"✅ Filtering complete! Jobs after filtering: {len(filtered_jobs)}")
        
        # Add to database and get only new jobs
        logger.info("Checking for new jobs in database...")
        new_jobs = db.add_jobs(filtered_jobs)
        logger.info(f"✅ Database check complete! New jobs found: {len(new_jobs)}")
        
        # Send email if we have new jobs
        if len(new_jobs) >= FILTER_CONFIG.get('min_jobs_for_email', 1):
            logger.info("Sending email notification...")
            
            # Initialize email notifier (supports both SMTP and SendGrid)
            sendgrid_api_key = os.getenv('SENDGRID_API_KEY')
            notifier = EmailNotifier(
                smtp_server=EMAIL_CONFIG.get('smtp_server'),
                smtp_port=EMAIL_CONFIG.get('smtp_port'),
                email=EMAIL_CONFIG['sender_email'],
                password=EMAIL_CONFIG.get('sender_password'),
                sendgrid_api_key=sendgrid_api_key
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
        logger.error(f"❌ Error in check_and_notify: {e}", exc_info=True)
        logger.error(f"Error type: {type(e).__name__}")
        import traceback
        logger.error(f"Full traceback:\n{traceback.format_exc()}")
        raise  # Re-raise to see in logs


def test_email():
    """Test email configuration"""
    logger.info("Testing email configuration...")
    
    try:
        sendgrid_api_key = os.getenv('SENDGRID_API_KEY')
        notifier = EmailNotifier(
            smtp_server=EMAIL_CONFIG.get('smtp_server'),
            smtp_port=EMAIL_CONFIG.get('smtp_port'),
            email=EMAIL_CONFIG['sender_email'],
            password=EMAIL_CONFIG.get('sender_password'),
            sendgrid_api_key=sendgrid_api_key
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
    logger.info(f"Starting at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Environment: {'Railway/Cloud' if os.getenv('RAILWAY_ENVIRONMENT') or os.getenv('RENDER') else 'Local'}")
    
    # Validate configuration
    # Check if email is still the default placeholder (means not configured)
    if EMAIL_CONFIG['sender_email'] == 'your_email@gmail.com' or not EMAIL_CONFIG['sender_email']:
        logger.error("⚠️  Please configure your email settings in config.py or environment variables!")
        logger.error("   Update EMAIL_CONFIG with your email credentials.")
        logger.error("   Or set environment variables: SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL")
        return
    
    # Log configuration status (without sensitive data)
    logger.info(f"Email configured: {EMAIL_CONFIG['sender_email']}")
    logger.info(f"Recipient: {EMAIL_CONFIG['recipient_email']}")
    logger.info(f"SMTP Server: {EMAIL_CONFIG['smtp_server']}:{EMAIL_CONFIG['smtp_port']}")
    logger.info(f"Check interval: {SCRAPING_CONFIG.get('check_interval_minutes', 30)} minutes")
    
    # Schedule job checks
    interval = SCRAPING_CONFIG.get('check_interval_minutes', 30)
    logger.info(f"Scheduling job checks every {interval} minutes...")
    
    schedule.every(interval).minutes.do(check_and_notify)
    
    # Run immediately on start
    logger.info("Running initial check...")
    check_and_notify()
    
    # Keep running
    logger.info(f"✅ Monitoring started. Checking every {interval} minutes...")
    logger.info("Process will run continuously. Press Ctrl+C to stop (if running locally).")
    
    try:
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute if any scheduled jobs are due
            except Exception as e:
                logger.error(f"Error in main loop: {e}", exc_info=True)
                logger.info("Continuing to run despite error...")
                time.sleep(60)  # Wait before continuing
    except KeyboardInterrupt:
        logger.info("\nStopping job scraper...")
        logger.info("Goodbye!")
    except Exception as e:
        logger.error(f"Fatal error in main loop: {e}", exc_info=True)
        logger.error("Process will exit. Check logs for details.")
        raise


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--test-email':
            test_email()
        elif sys.argv[1] == '--test':
            # Run diagnostic tests
            from test_deployment import main as run_tests
            run_tests()
        else:
            print("Usage: python main.py [--test-email|--test]")
            sys.exit(1)
    else:
        main()

