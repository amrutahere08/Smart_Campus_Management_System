"""
Web scraper for Chanakya University website
Collects comprehensive data about university, schools, programs, faculty, etc.
"""
import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urljoin, urlparse
import re

class ChanakyaUniversityScraper:
    def __init__(self):
        self.base_url = "https://chanakyauniversity.edu.in"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        self.data = {
            'university': {},
            'schools': [],
            'programs': [],
            'faculty': [],
            'admissions': {},
            'facilities': [],
            'research': [],
            'events': []
        }
    
    def fetch_page(self, url):
        """Fetch a page with error handling"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            return None
    
    def clean_text(self, text):
        """Clean and normalize text"""
        if not text:
            return ""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def scrape_about(self):
        """Scrape university overview and about information"""
        print("Scraping university overview...")
        soup = self.fetch_page(f"{self.base_url}/about/")
        
        if soup:
            # Extract main content
            content = soup.find('div', class_='entry-content') or soup.find('main')
            if content:
                paragraphs = content.find_all('p')
                about_text = ' '.join([self.clean_text(p.get_text()) for p in paragraphs])
                
                self.data['university'] = {
                    'name': 'Chanakya University',
                    'location': 'Bangalore, Karnataka, India',
                    'about': about_text[:1000] if about_text else 'A leading university in Bangalore',
                    'website': self.base_url
                }
    
    def scrape_schools(self):
        """Scrape information about all schools"""
        print("Scraping schools information...")
        
        schools_info = [
            {
                'name': 'School of Arts, Humanities and Social Sciences',
                'url': f"{self.base_url}/schools/school-of-arts-humanities-and-social-sciences/",
                'short_name': 'SAHSS',
                'dean': 'Prof. Sandeep Nair',
                'dean_cabin': 'Cabin 428, 4th Floor, Academic Block 1'
            },
            {
                'name': 'School of Management Sciences',
                'url': f"{self.base_url}/schools/school-of-management-sciences/",
                'short_name': 'SMS',
                'dean': 'Dr. Dinesh Shenoy',
                'dean_cabin': 'Cabin 427, 4th Floor, Academic Block 1'
            },
            {
                'name': 'School of Mathematics and Natural Sciences',
                'url': f"{self.base_url}/schools/school-of-mathematics-and-natural-sciences/",
                'short_name': 'SMNS',
                'dean': 'Not specified',
                'dean_cabin': 'Please contact school office'
            },
            {
                'name': 'School of Law, Governance and Public Policy',
                'url': f"{self.base_url}/schools/school-of-public-policy-legal-studies/",
                'short_name': 'SLGPP',
                'dean': 'Prof. Chetan Basavaraj Singai',
                'dean_cabin': 'Cabin 426, 4th Floor, Academic Block 1'
            },
            {
                'name': 'School of Biosciences',
                'url': f"{self.base_url}/bioscience/",
                'short_name': 'SB',
                'dean': 'Not specified',
                'dean_cabin': 'Please contact school office'
            },
            {
                'name': 'School of Engineering',
                'url': f"{self.base_url}/schools/school-of-engineering/",
                'short_name': 'SE',
                'dean': 'Not specified',
                'dean_cabin': 'Academic Block 2'
            }
        ]
        
        for school_info in schools_info:
            soup = self.fetch_page(school_info['url'])
            if soup:
                content = soup.find('div', class_='entry-content') or soup.find('main')
                description = ""
                programs = []
                faculty = []
                
                if content:
                    paragraphs = content.find_all('p')
                    description = ' '.join([self.clean_text(p.get_text()) for p in paragraphs[:3]])
                    
                    # Try to find programs/courses
                    lists = content.find_all(['ul', 'ol'])
                    for lst in lists:
                        items = lst.find_all('li')
                        for item in items:
                            text = self.clean_text(item.get_text())
                            if text and len(text) < 200:
                                programs.append(text)
                    
                    # Try to extract faculty names
                    headings = content.find_all(['h3', 'h4', 'h5'])
                    for heading in headings:
                        text = self.clean_text(heading.get_text())
                        if any(keyword in text.lower() for keyword in ['prof', 'dr', 'faculty', 'professor']):
                            if len(text) < 100:
                                faculty.append(text)
                
                self.data['schools'].append({
                    'name': school_info['name'],
                    'short_name': school_info['short_name'],
                    'dean': school_info['dean'],
                    'dean_location': school_info['dean_cabin'],
                    'description': description[:500] if description else f"The {school_info['name']} at Chanakya University offers comprehensive programs in its field.",
                    'programs': programs[:10],
                    'faculty_highlights': faculty[:5],
                    'url': school_info['url']
                })
            
            time.sleep(1)  # Be polite to the server
    
    def scrape_programs(self):
        """Scrape programs and courses"""
        print("Scraping programs information...")
        soup = self.fetch_page(f"{self.base_url}/programs/")
        
        if soup:
            # Look for program listings
            content = soup.find('div', class_='entry-content') or soup.find('main')
            if content:
                # Find all headings and their content
                headings = content.find_all(['h2', 'h3', 'h4'])
                for heading in headings:
                    program_name = self.clean_text(heading.get_text())
                    if program_name and len(program_name) < 200:
                        # Get description from next sibling
                        description = ""
                        next_elem = heading.find_next_sibling()
                        if next_elem and next_elem.name == 'p':
                            description = self.clean_text(next_elem.get_text())
                        
                        self.data['programs'].append({
                            'name': program_name,
                            'description': description[:300] if description else "",
                            'university': 'Chanakya University'
                        })
    
    def scrape_admissions(self):
        """Scrape admissions information"""
        print("Scraping admissions information...")
        soup = self.fetch_page(f"{self.base_url}/admissions/")
        
        if soup:
            content = soup.find('div', class_='entry-content') or soup.find('main')
            if content:
                paragraphs = content.find_all('p')
                admission_text = ' '.join([self.clean_text(p.get_text()) for p in paragraphs])
                
                self.data['admissions'] = {
                    'process': admission_text[:800] if admission_text else "Visit the admissions page for details",
                    'website': f"{self.base_url}/admissions/",
                    'contact': 'admissions@chanakyauniversity.edu.in'
                }
    
    def scrape_homepage(self):
        """Scrape homepage for general information"""
        print("Scraping homepage...")
        soup = self.fetch_page(self.base_url)
        
        if soup:
            # Extract key highlights
            highlights = []
            content = soup.find('main') or soup.find('body')
            if content:
                # Look for key sections
                sections = content.find_all(['section', 'div'], class_=re.compile(r'(highlight|feature|about)'))
                for section in sections[:5]:
                    text = self.clean_text(section.get_text())
                    if text and 50 < len(text) < 500:
                        highlights.append(text)
            
            if highlights:
                self.data['university']['highlights'] = highlights
    
    def scrape_all(self):
        """Run all scraping tasks"""
        print("Starting Chanakya University data scraping...")
        print("=" * 60)
        
        self.scrape_homepage()
        self.scrape_about()
        self.scrape_schools()
        self.scrape_programs()
        self.scrape_admissions()
        
        print("=" * 60)
        print("Scraping completed!")
        return self.data
    
    def save_to_file(self, filename='data/chanakya_knowledge.json'):
        """Save scraped data to JSON file"""
        import os
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Data saved to {filename}")
        print(f"   - Schools: {len(self.data['schools'])}")
        print(f"   - Programs: {len(self.data['programs'])}")
        print(f"   - Admissions info: {'Yes' if self.data['admissions'] else 'No'}")

if __name__ == "__main__":
    scraper = ChanakyaUniversityScraper()
    data = scraper.scrape_all()
    scraper.save_to_file()
    
    print("\n" + "=" * 60)
    print("Summary of scraped data:")
    print(json.dumps({
        'schools_count': len(data['schools']),
        'programs_count': len(data['programs']),
        'has_university_info': bool(data['university']),
        'has_admissions_info': bool(data['admissions'])
    }, indent=2))
