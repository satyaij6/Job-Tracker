"""
Email notification module for sending job alerts
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailNotifier:
    """Handles sending email notifications for new job listings"""
    
    def __init__(self, smtp_server: str, smtp_port: int, email: str, password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email = email
        self.password = password
    
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
    
    def send_email(self, recipient: str, jobs: List[Dict], subject: str = None):
        """Send email notification with job listings"""
        if not jobs:
            logger.info("No jobs to send, skipping email")
            return
        
        if subject is None:
            subject = f"Hi Satya, 🎯 {len(jobs)} New Job Listing(s) Found!"
        
        try:
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
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email, self.password)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully to {recipient} with {len(jobs)} jobs")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email: {e}")
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

