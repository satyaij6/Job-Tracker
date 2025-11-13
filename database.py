"""
Database module for storing and tracking job listings
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JobDatabase:
    """SQLite database for tracking job listings"""
    
    def __init__(self, db_path: str = "jobs.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                company TEXT,
                url TEXT UNIQUE NOT NULL,
                source TEXT,
                scraped_at TEXT,
                notified INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_url ON jobs(url)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_notified ON jobs(notified)
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized")
    
    def job_exists(self, url: str) -> bool:
        """Check if a job with the given URL already exists"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM jobs WHERE url = ?', (url,))
        count = cursor.fetchone()[0]
        
        conn.close()
        return count > 0
    
    def add_job(self, job: Dict) -> bool:
        """Add a new job to the database. Returns True if job was new, False if it already existed"""
        if self.job_exists(job['url']):
            return False
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO jobs (title, company, url, source, scraped_at, notified)
                VALUES (?, ?, ?, ?, ?, 0)
            ''', (
                job.get('title', ''),
                job.get('company', 'Unknown'),
                job.get('url', ''),
                job.get('source', 'Unknown'),
                job.get('scraped_at', datetime.now().isoformat())
            ))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            conn.close()
            return False
        except Exception as e:
            logger.error(f"Error adding job to database: {e}")
            conn.close()
            return False
    
    def add_jobs(self, jobs: List[Dict]) -> List[Dict]:
        """Add multiple jobs and return only the new ones"""
        new_jobs = []
        for job in jobs:
            if self.add_job(job):
                new_jobs.append(job)
        return new_jobs
    
    def mark_as_notified(self, job_id: int):
        """Mark a job as notified"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('UPDATE jobs SET notified = 1 WHERE id = ?', (job_id,))
        conn.commit()
        conn.close()
    
    def get_unnotified_jobs(self) -> List[Dict]:
        """Get all jobs that haven't been notified yet"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM jobs WHERE notified = 0 ORDER BY created_at DESC
        ''')
        
        rows = cursor.fetchall()
        jobs = [dict(row) for row in rows]
        
        conn.close()
        return jobs
    
    def get_stats(self) -> Dict:
        """Get database statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM jobs')
        total = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM jobs WHERE notified = 0')
        unnotified = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM jobs WHERE notified = 1')
        notified = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_jobs': total,
            'unnotified_jobs': unnotified,
            'notified_jobs': notified
        }

