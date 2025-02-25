from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import html2text
import time
import random
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
from urllib.parse import urljoin, urlparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crawler.log'),
        logging.StreamHandler()
    ]
)

# Load environment variables
load_dotenv()
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')

HEADLESS_OPTIONS = [
    "--headless=new",
    "--disable-gpu",
    "--disable-dev-shm-usage",
    "--window-size=1920,1080",
    "--disable-search-engine-choice-screen",
    "--disable-blink-features=AutomationControlled",
    "--lang=or"
]

SYSTEM_MESSAGE = """You are an intelligent multilingual text extraction assistant.
Extract structured information from the given webpage content and convert it into a pure JSON format.
Include both English and Odia text where available.
The JSON should contain:
1. Page title
2. Main content
3. Any important links or references
4. Forms or application details if present
5. Contact information if available
Return only the JSON output with no additional text."""

class MultilingualWebCrawler:
    def __init__(self, base_url, allowed_urls=None):
        """Initialize the crawler with base URL and allowed URLs."""
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.visited_urls = set()
        self.content_database = {}
        self.allowed_urls = set(allowed_urls) if allowed_urls else {base_url}
        
        # Configure Gemini AI
        try:
            genai.configure()
            self.model = genai.GenerativeModel("gemini-1.5-flash")
        except Exception as e:
            logging.error(f"Error configuring Gemini AI: {str(e)}")
            raise
        
    def setup_driver(self):
        """Setup and configure Chrome WebDriver."""
        try:
            options = Options()
            for option in HEADLESS_OPTIONS:
                options.add_argument(option)
            options.add_argument('--accept-languages=or,en')
            options.add_argument('--charset=UTF-8')
            service = Service(ChromeDriverManager().install())
            return webdriver.Chrome(service=service, options=options)
        except Exception as e:
            logging.error(f"Error setting up WebDriver: {str(e)}")
            raise

    def is_valid_url(self, url):
        """Check if URL is valid and is in the allowed URLs list."""
        try:
            if not url:
                return False
                
            parsed = urlparse(url)
            if parsed.netloc != self.domain:
                return False
                
            # Check if URL matches any allowed pattern
            if not self.allowed_urls:
                return True
                
            # Check if the URL or any of its parent paths are in allowed_urls
            current_path = url
            while current_path:
                if current_path in self.allowed_urls:
                    return True
                parsed = urlparse(current_path)
                path_parts = parsed.path.rstrip('/').split('/')
                if len(path_parts) <= 1:
                    break
                new_path = '/'.join(path_parts[:-1])
                current_path = f"{parsed.scheme}://{parsed.netloc}{new_path}"
                
            return False
                
        except Exception as e:
            logging.error(f"Error validating URL {url}: {str(e)}")
            return False

    def extract_links(self, driver):
        """Extract all valid links from the current page."""
        links = set()
        try:
            elements = driver.find_elements(By.TAG_NAME, "a")
            for element in elements:
                href = element.get_attribute("href")
                if href and self.is_valid_url(href) and href not in self.visited_urls:
                    links.add(href)
        except Exception as e:
            logging.error(f"Error extracting links: {str(e)}")
        return links

    def clean_html_content(self, html_content):
        """Clean HTML with enhanced encoding handling."""
        try:
            soup = BeautifulSoup(html_content, 'html.parser', from_encoding='utf-8')
            
            # Remove unwanted elements
            for element in soup.find_all(['script', 'style', 'iframe', 'nav']):
                element.decompose()
            
            # Try to find main content area
            main_content = (
                soup.find('main') or 
                soup.find('article') or 
                soup.find('div', class_='content') or 
                soup.find('div', id='content') or 
                soup
            )
            
            return str(main_content)
        except Exception as e:
            logging.error(f"Error cleaning HTML content: {str(e)}")
            return html_content

    def convert_html_to_text(self, html_content):
        """Convert HTML to text with better Unicode handling."""
        try:
            cleaned_html = self.clean_html_content(html_content)
            converter = html2text.HTML2Text()
            converter.ignore_links = False
            converter.unicode_snob = True
            converter.body_width = 0
            return converter.handle(cleaned_html)
        except Exception as e:
            logging.error(f"Error converting HTML to text: {str(e)}")
            return ""

    def process_with_gemini(self, text, url):
        """Process text through Gemini with enhanced context."""
        try:
            prompt = f"{SYSTEM_MESSAGE}\n\nURL: {url}\n\nPage content:\n{text}"
            response = self.model.generate_content(prompt)
            
            try:
                json_response = json.loads(response.text)
                return json.dumps(json_response, ensure_ascii=False, indent=2)
            except json.JSONDecodeError:
                logging.warning(f"Invalid JSON response from Gemini for URL {url}")
                return response.text
            
        except Exception as e:
            logging.error(f"Error processing with Gemini: {str(e)}")
            return None

    def fetch_page_content(self, url, driver):
        """Fetch content from a single page in both languages."""
        try:
            wait = WebDriverWait(driver, 10)
            content = {'url': url, 'english': None, 'odia': None}
            
            # Navigate to page
            driver.get(url)
            time.sleep(3)

            try:
                # Try to find language selector
                language_select = wait.until(
                    EC.presence_of_element_located((By.ID, "lang_select"))
                )
                select = Select(language_select)

                # Get English content
                select.select_by_value("en")
                time.sleep(3)
                english_html = driver.page_source
                english_text = self.convert_html_to_text(english_html)
                content['english'] = self.process_with_gemini(english_text, url)

                # Get Odia content
                select.select_by_value("od")
                time.sleep(3)
                odia_html = driver.page_source
                odia_text = self.convert_html_to_text(odia_html)
                content['odia'] = self.process_with_gemini(odia_text, url)

            except Exception as e:
                # If language selector not found, process current page content
                logging.warning(f"Language selector not found on {url}, processing current content: {str(e)}")
                html = driver.page_source
                text = self.convert_html_to_text(html)
                content['english'] = self.process_with_gemini(text, url)

            return content

        except Exception as e:
            logging.error(f"Error fetching content from {url}: {str(e)}")
            return None

    def crawl(self, max_pages=10):
        """Crawl the website starting from base_url."""
        driver = None
        try:
            driver = self.setup_driver()
            pages_to_visit = {self.base_url}
            
            while pages_to_visit and len(self.visited_urls) < max_pages:
                current_url = pages_to_visit.pop()
                
                if current_url in self.visited_urls:
                    continue
                
                logging.info(f"Processing page: {current_url}")
                self.visited_urls.add(current_url)
                
                # Fetch content from current page
                content = self.fetch_page_content(current_url, driver)
                if content:
                    self.content_database[current_url] = content
                
                # Extract new links
                new_links = self.extract_links(driver)
                pages_to_visit.update(new_links)
                
                # Random delay between requests
                time.sleep(random.uniform(2, 4))
                
        except Exception as e:
            logging.error(f"Crawling error: {str(e)}")
        finally:
            if driver:
                driver.quit()
            
        return self.content_database

def save_results(content_database, output_file="crawl_results.json"):
    """Save crawled content to a JSON file."""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(content_database, f, ensure_ascii=False, indent=2)
        logging.info(f"Results saved to {output_file}")
    except Exception as e:
        logging.error(f"Error saving results: {str(e)}")

def get_user_allowed_urls():
    """Get allowed URLs from user input."""
    print("Enter the URLs you want to crawl (one per line).")
    print("Press Enter twice when you're done:")
    
    allowed_urls = set()
    while True:
        url = input().strip()
        if not url:
            break
        allowed_urls.add(url)
    
    return allowed_urls

def main():
    try:
        base_url = "https://ashish................."  # enter your link to scrape
        max_pages = 10  # Adjust this number based on your needs
        
        # Get allowed URLs from user
        print("Please enter the URLs you want to crawl:")
        allowed_urls = get_user_allowed_urls()
        
        # Initialize crawler with allowed URLs
        crawler = MultilingualWebCrawler(base_url, allowed_urls)
        content_database = crawler.crawl(max_pages=max_pages)
        
        # Save results
        save_results(content_database)
        
        # Print summary
        print(f"\nCrawling completed:")
        print(f"Total pages processed: {len(content_database)}")
        print(f"Pages visited:")
        for url in content_database.keys():
            print(f"- {url}")
            
    except Exception as e:
        logging.error(f"Main execution error: {str(e)}")
        raise

if __name__ == "__main__":
    main()