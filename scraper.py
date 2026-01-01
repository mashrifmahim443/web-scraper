"""
Web Scraper Module
Handles fetching and parsing website content
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re


class WebScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def is_valid_url(self, url):
        """Check if URL is valid"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    def fetch_url(self, url, timeout=10):
        """Fetch content from a URL"""
        if not self.is_valid_url(url):
            raise ValueError(f"Invalid URL: {url}")
        
        try:
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching URL: {str(e)}")
    
    def extract_text(self, html_content):
        """Extract clean text from HTML content"""
        soup = BeautifulSoup(html_content, 'lxml')
        
        # Remove script and style elements
        for script in soup(["script", "style", "meta", "link", "noscript"]):
            script.decompose()
        
        # Get text
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    
    def extract_structured_content(self, html_content):
        """Extract structured content (title, headings, paragraphs)"""
        soup = BeautifulSoup(html_content, 'lxml')
        
        # Remove script and style elements
        for script in soup(["script", "style", "meta", "link", "noscript"]):
            script.decompose()
        
        content = {
            'title': '',
            'headings': [],
            'paragraphs': [],
            'links': []
        }
        
        # Extract title
        title_tag = soup.find('title')
        if title_tag:
            content['title'] = title_tag.get_text().strip()
        
        # Extract headings
        for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            heading_text = heading.get_text().strip()
            if heading_text:
                content['headings'].append(heading_text)
        
        # Extract paragraphs
        for para in soup.find_all('p'):
            para_text = para.get_text().strip()
            if para_text and len(para_text) > 20:  # Filter out very short paragraphs
                content['paragraphs'].append(para_text)
        
        # Extract main text content
        main_text = self.extract_text(html_content)
        
        return {
            'structured': content,
            'full_text': main_text
        }
    
    def scrape(self, url, structured=False):
        """
        Scrape a website and return its content
        
        Args:
            url: URL to scrape
            structured: If True, return structured content; if False, return plain text
        
        Returns:
            Dictionary with scraped content
        """
        html_content = self.fetch_url(url)
        
        if structured:
            content = self.extract_structured_content(html_content)
        else:
            text = self.extract_text(html_content)
            content = {
                'url': url,
                'text': text,
                'length': len(text)
            }
        
        return content

