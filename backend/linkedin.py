\
# linkedin.py - updated to filter jobs posted in the last 24 hours and support env overrides
import os, time, urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
from utils import safe_find, choose_resume_for_keyword

load_dotenv()
CHROME_PROFILE_DIR = os.getenv('CHROME_PROFILE_DIR', r"C:\\autoapply\\chrome_profile2")
RESUME_DEFAULT = os.getenv('RESUME_PATH')
LOCATION = os.getenv('LOCATION','Bangalore')

JOB_KEYWORDS = [
    'Frontend Developer','React Developer','MERN Developer','Junior Developer',
    'Entry Level','Html Css Developer','Python Developer','Software Engineer',
    'Web Developer intern','Full Stack Intern','Software Engineer Fresher','Junior Web Developer'
]
MAX_APPLIES = int(os.getenv('MAX_APPLIES','4'))
WAIT_SHORT = 1.0
WAIT_LONG = 2.5

def open_driver():
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={CHROME_PROFILE_DIR}")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    return driver

def run():
    driver = open_driver()
    applied = 0
    try:
        keywords = [os.getenv('JOB_KEYWORD_OVERRIDE')] if os.getenv('JOB_KEYWORD_OVERRIDE') else JOB_KEYWORDS
        for kw in keywords:
            if applied >= MAX_APPLIES: break
            q = urllib.parse.quote(kw)
            url = f"https://www.linkedin.com/jobs/search/?keywords={q}&location={LOCATION}&f_TPR=r86400&sortBy=DD"
            driver.get(url); time.sleep(WAIT_LONG)
            print('Searching LinkedIn for:', kw)
            cards = driver.find_elements(By.CSS_SELECTOR, 'ul.jobs-search__results-list li')
            if not cards:
                cards = driver.find_elements(By.CSS_SELECTOR, '.jobs-search-results__list-item')
            for card in cards[:5]:
                try:
                    title = card.text.split('\\n')[0][:120]
                except:
                    title = '<no-title>'
                print('Found job:', title)
            print('LinkedIn done. Applied:', applied)
    finally:
        driver.quit()

if __name__ == '__main__':
    run()
