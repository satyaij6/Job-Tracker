"""
Job Scraper Module
Scrapes new grad and internship listings from Indian job sites
"""

import requests
from bs4 import BeautifulSoup
import time
import re
from datetime import datetime
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JobScraper:
    """Base class for job scrapers"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def scrape(self, keywords: List[str] = None) -> List[Dict]:
        """Override in subclasses"""
        raise NotImplementedError


class LinkedInScraper(JobScraper):
    """Scraper for LinkedIn job listings"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.linkedin.com/jobs/search"
    
    def scrape(self, keywords: List[str] = None) -> List[Dict]:
        """Scrape LinkedIn jobs"""
        jobs = []
        keywords = keywords or ["new grad", "fresher", "internship", "entry level"]
        
        for keyword in keywords:
            try:
                params = {
                    'keywords': f"{keyword} India",
                    'location': 'India',
                    'f_TPR': 'r86400',  # Past 24 hours
                    'f_E': '2,1',  # Entry level and internship
                    'start': 0
                }
                
                response = requests.get(self.base_url, params=params, headers=self.headers, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    job_cards = soup.find_all('div', class_='base-card')
                    
                    for card in job_cards[:20]:  # Limit to first 20 results
                        try:
                            title_elem = card.find('h3', class_='base-search-card__title')
                            company_elem = card.find('h4', class_='base-search-card__subtitle')
                            link_elem = card.find('a', class_='base-card__full-link')
                            
                            if title_elem and link_elem:
                                job = {
                                    'title': title_elem.get_text(strip=True),
                                    'company': company_elem.get_text(strip=True) if company_elem else 'Unknown',
                                    'url': link_elem.get('href', '').split('?')[0],
                                    'source': 'LinkedIn',
                                    'scraped_at': datetime.now().isoformat()
                                }
                                jobs.append(job)
                        except Exception as e:
                            logger.error(f"Error parsing LinkedIn job card: {e}")
                            continue
                
                time.sleep(2)  # Be respectful with requests
            except Exception as e:
                logger.error(f"Error scraping LinkedIn for keyword '{keyword}': {e}")
                continue
        
        return jobs


class InternshalaScraper(JobScraper):
    """Scraper for Internshala internship listings"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://internshala.com/internships"
    
    def scrape(self, keywords: List[str] = None) -> List[Dict]:
        """Scrape Internshala internships"""
        jobs = []
        
        try:
            params = {
                'location': 'india',
                'preference': 'all'
            }
            
            response = requests.get(self.base_url, params=params, headers=self.headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                internship_cards = soup.find_all('div', class_='internship_meta')
                
                for card in internship_cards[:30]:  # Limit results
                    try:
                        title_elem = card.find('h3', class_='heading_4_5')
                        company_elem = card.find('a', class_='link_display_like_text')
                        link_elem = card.find('a', class_='view_detail_button')
                        
                        if title_elem:
                            job = {
                                'title': title_elem.get_text(strip=True),
                                'company': company_elem.get_text(strip=True) if company_elem else 'Unknown',
                                'url': f"https://internshala.com{link_elem.get('href', '')}" if link_elem else '',
                                'source': 'Internshala',
                                'scraped_at': datetime.now().isoformat()
                            }
                            jobs.append(job)
                    except Exception as e:
                        logger.error(f"Error parsing Internshala card: {e}")
                        continue
            
            time.sleep(2)
        except Exception as e:
            logger.error(f"Error scraping Internshala: {e}")
        
        return jobs


class NaukriScraper(JobScraper):
    """Scraper for Naukri.com job listings"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.naukri.com/jobs-in-india"
    
    def scrape(self, keywords: List[str] = None) -> List[Dict]:
        """Scrape Naukri jobs"""
        jobs = []
        keywords = keywords or ["fresher", "entry level", "trainee"]
        
        for keyword in keywords:
            try:
                params = {
                    'k': keyword,
                    'l': 'india',
                    'experience': '0'  # Fresher jobs
                }
                
                response = requests.get(self.base_url, params=params, headers=self.headers, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    job_cards = soup.find_all('article', class_='jobTuple')
                    
                    for card in job_cards[:20]:
                        try:
                            title_elem = card.find('a', class_='title')
                            company_elem = card.find('a', class_='subTitle')
                            
                            if title_elem:
                                job = {
                                    'title': title_elem.get_text(strip=True),
                                    'company': company_elem.get_text(strip=True) if company_elem else 'Unknown',
                                    'url': title_elem.get('href', ''),
                                    'source': 'Naukri',
                                    'scraped_at': datetime.now().isoformat()
                                }
                                jobs.append(job)
                        except Exception as e:
                            logger.error(f"Error parsing Naukri job card: {e}")
                            continue
                
                time.sleep(2)
            except Exception as e:
                logger.error(f"Error scraping Naukri for keyword '{keyword}': {e}")
                continue
        
        return jobs


class IndeedScraper(JobScraper):
    """Scraper for Indeed job listings"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://in.indeed.com/jobs"
    
    def scrape(self, keywords: List[str] = None) -> List[Dict]:
        """Scrape Indeed jobs"""
        jobs = []
        keywords = keywords or ["fresher", "entry level", "intern", "new grad"]
        
        for keyword in keywords:
            try:
                params = {
                    'q': f"{keyword} India",
                    'l': 'India',
                    'fromage': '1',  # Last 24 hours
                    'explvl': 'entry_level'
                }
                
                response = requests.get(self.base_url, params=params, headers=self.headers, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    job_cards = soup.find_all('div', class_='job_seen_beacon')
                    
                    for card in job_cards[:20]:
                        try:
                            title_elem = card.find('h2', class_='jobTitle')
                            company_elem = card.find('span', class_='companyName')
                            link_elem = card.find('a', class_='jcs-JobTitle')
                            
                            if title_elem and link_elem:
                                job = {
                                    'title': title_elem.get_text(strip=True),
                                    'company': company_elem.get_text(strip=True) if company_elem else 'Unknown',
                                    'url': f"https://in.indeed.com{link_elem.get('href', '')}",
                                    'source': 'Indeed',
                                    'scraped_at': datetime.now().isoformat()
                                }
                                jobs.append(job)
                        except Exception as e:
                            logger.error(f"Error parsing Indeed job card: {e}")
                            continue
                
                time.sleep(2)
            except Exception as e:
                logger.error(f"Error scraping Indeed for keyword '{keyword}': {e}")
                continue
        
        return jobs


def scrape_all_jobs(keywords: List[str] = None) -> List[Dict]:
    """Scrape jobs from all sources"""
    all_jobs = []
    scrapers = [
        LinkedInScraper(),
        InternshalaScraper(),
        NaukriScraper(),
        IndeedScraper()
    ]
    
    for scraper in scrapers:
        try:
            logger.info(f"Scraping {scraper.__class__.__name__}...")
            jobs = scraper.scrape(keywords)
            all_jobs.extend(jobs)
            logger.info(f"Found {len(jobs)} jobs from {scraper.__class__.__name__}")
        except Exception as e:
            logger.error(f"Error with {scraper.__class__.__name__}: {e}")
            continue
    
    return all_jobs

