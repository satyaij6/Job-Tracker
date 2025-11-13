"""
Email notification module for sending job alerts
Supports both SMTP and SendGrid API
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Optional
import logging
from datetime import datetime
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailNotifier:
    """Handles sending email notifications for new job listings"""
    
    def __init__(self, smtp_server: str = None, smtp_port: int = None, email: str = None, password: str = None, sendgrid_api_key: str = None):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email = email
        self.password = password
        self.sendgrid_api_key = sendgrid_api_key or os.getenv('SENDGRID_API_KEY')
        
        # Check if SendGrid should be used
        self.use_sendgrid = os.getenv('USE_SENDGRID', 'false').lower() == 'true' or self.sendgrid_api_key is not None
    
    def create_email_body(self, jobs: List[Dict]) -> str:
        """Create HTML email body with job listings"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
                .job-container {{ margin: 20px 0; padding: 15px; border-left: 4px solid #4CAF50; background-color: #f9f9f9; }}
                .job-title {{ font-size: 18px; font-weight: bold; color: #2c3e50; margin-bottom: 5px; }}
                .job-company {{ color: #7f8c8d; margin-bottom: 10px; }}
                .job-link {{ color: #3498db; text-decoration: none; }}
                .job-link:hover {{ text-decoration: underline; }}
                .job-source {{ display: inline-block; background-color: #3498db; color: white; padding: 3px 8px; border-radius: 3px; font-size: 12px; margin-top: 5px; }}
                .footer {{ margin-top: 30px; padding: 20px; text-align: center; color: #7f8c8d; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🚀 New Job Listings Found!</h1>
                <p>{len(jobs)} new job(s) posted in the last check</p>
            </div>
        """
        
        for job in jobs:
            html += f"""
            <div class="job-container">
                <div class="job-title">{job.get('title', 'N/A')}</div>
                <div class="job-company">Company: {job.get('company', 'Unknown')}</div>
                <div class="job-source">{job.get('source', 'Unknown')}</div>
                <div style="margin-top: 10px;">
                    <a href="{job.get('url', '#')}" class="job-link" target="_blank">View Job →</a>
                </div>
            </div>
            """
        
        html += f"""
            <div class="footer">
                <p>Scraped at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p>Good luck with your applications! 🎯</p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def send_email_via_sendgrid(self, recipient: str, jobs: List[Dict], subject: str) -> bool:
        """Send email using SendGrid API"""
        try:
            from sendgrid import SendGridAPIClient
            from sendgrid.helpers.mail import Mail, Content
            
            if not self.sendgrid_api_key:
                logger.error("❌ SendGrid API key not found")
                return False
            
            logger.info("Sending email via SendGrid API...")
            
            # Create email content
            html_content = self.create_email_body(jobs)
            
            text_content = f"Found {len(jobs)} new job listing(s):\n\n"
            for job in jobs:
                text_content += f"{job.get('title', 'N/A')} at {job.get('company', 'Unknown')}\n"
                text_content += f"Link: {job.get('url', '')}\n\n"
            
            from_email_address = self.email or os.getenv('SENDER_EMAIL', 'noreply@example.com')
            if not from_email_address:
                logger.error("❌ No sender email configured for SendGrid")
                return False
            
            # Create SendGrid message (html + plain text)
            message = Mail(
                from_email=from_email_address,
                to_emails=recipient,
                subject=subject,
                html_content=html_content
            )
            # Add plain text version for email clients that don't support HTML
            message.add_content(Content("text/plain", text_content))
            
            # Send email
            sg = SendGridAPIClient(self.sendgrid_api_key)
            response = sg.send(message)
            
            if response.status_code in [200, 202]:
                logger.info(f"✅ Email sent successfully via SendGrid to {recipient} with {len(jobs)} jobs")
                return True
            else:
                logger.error(f"❌ SendGrid API error: Status {response.status_code}")
                logger.error(f"Response: {response.body}")
                return False
                
        except ImportError:
            logger.error("❌ SendGrid package not installed. Run: pip install sendgrid")
            return False
        except Exception as e:
            logger.error(f"❌ Error sending email via SendGrid: {e}")
            return False
    
    def send_email(self, recipient: str, jobs: List[Dict], subject: str = None, retries: int = 3):
        """Send email notification with job listings"""
        if not jobs:
            logger.info("No jobs to send, skipping email")
            return False
        
        if subject is None:
            subject = f"Hi Satya, 🎯 {len(jobs)} New Job Listing(s) Found!"
        
        # Try SendGrid first if configured
        if self.use_sendgrid:
            logger.info("Using SendGrid API for email delivery...")
            success = self.send_email_via_sendgrid(recipient, jobs, subject)
            if success:
                return True
            else:
                logger.warning("SendGrid failed, falling back to SMTP...")
        
        # Fall back to SMTP if SendGrid not available or failed
        
        # Try multiple SMTP methods
        smtp_methods = [
            {'port': 587, 'use_tls': True, 'use_ssl': False},
            {'port': 465, 'use_tls': False, 'use_ssl': True},
            {'port': 25, 'use_tls': True, 'use_ssl': False},
        ]
        
        for attempt in range(retries):
            for method in smtp_methods:
                try:
                    logger.info(f"Attempting to send email (attempt {attempt + 1}/{retries}) via {self.smtp_server}:{method['port']}...")
                    
                    msg = MIMEMultipart('alternative')
                    msg['Subject'] = subject
                    msg['From'] = self.email
                    msg['To'] = recipient
                    
                    # Create both plain text and HTML versions
                    text = f"Found {len(jobs)} new job listing(s):\n\n"
                    for job in jobs:
                        text += f"{job.get('title', 'N/A')} at {job.get('company', 'Unknown')}\n"
                        text += f"Link: {job.get('url', '')}\n\n"
                    
                    html = self.create_email_body(jobs)
                    
                    part1 = MIMEText(text, 'plain')
                    part2 = MIMEText(html, 'html')
                    
                    msg.attach(part1)
                    msg.attach(part2)
                    
                    # Try SSL first (port 465), then TLS (port 587)
                    if method['use_ssl']:
                        server = smtplib.SMTP_SSL(self.smtp_server, method['port'], timeout=30)
                    else:
                        server = smtplib.SMTP(self.smtp_server, method['port'], timeout=30)
                    
                    if method['use_tls']:
                        server.starttls()
                    
                    server.login(self.email, self.password)
                    server.send_message(msg)
                    server.quit()
                    
                    logger.info(f"✅ Email sent successfully to {recipient} with {len(jobs)} jobs")
                    return True
                    
                except smtplib.SMTPConnectError as e:
                    logger.warning(f"Connection error on port {method['port']}: {e}")
                    continue
                except smtplib.SMTPAuthenticationError as e:
                    logger.error(f"❌ Authentication failed: {e}")
                    logger.error("   Check your email and App Password in Railway environment variables")
                    return False
                except OSError as e:
                    error_msg = str(e).lower()
                    if 'network is unreachable' in error_msg or '101' in error_msg:
                        logger.warning(f"Network unreachable on port {method['port']}: {e}")
                        logger.warning("   Railway may be blocking SMTP connections. Trying alternative method...")
                        continue
                    else:
                        logger.warning(f"Network error on port {method['port']}: {e}")
                        continue
                except Exception as e:
                    logger.warning(f"Error on port {method['port']}: {type(e).__name__}: {e}")
                    continue
            
            if attempt < retries - 1:
                wait_time = (attempt + 1) * 5  # Wait 5, 10, 15 seconds
                logger.info(f"Waiting {wait_time} seconds before retry...")
                import time
                time.sleep(wait_time)
        
        logger.error(f"❌ Failed to send email after {retries} attempts")
        logger.error("   Possible issues:")
        logger.error("   1. Railway is blocking SMTP connections (port 587/465)")
        logger.error("   2. Network connectivity issues")
        logger.error("   3. Gmail App Password is incorrect")
        logger.error("   4. Firewall blocking outbound SMTP")
        return False
    
    def send_test_email(self, recipient: str):
        """Send a test email to verify configuration"""
        test_jobs = [{
            'title': 'Test Job Listing',
            'company': 'Test Company',
            'url': 'https://example.com',
            'source': 'Test Source',
            'scraped_at': datetime.now().isoformat()
        }]
        
        return self.send_email(recipient, test_jobs, "🧪 Test Email - Job Scraper")

