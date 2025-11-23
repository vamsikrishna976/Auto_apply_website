\
# indeed.py - updated to use chrome profile and filter recent jobs
import os, time, urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
from utils import safe_find, choose_resume_for_keyword

load_dotenv()

CHROME_PROFILE_DIR = os.getenv('CHROME_PROFILE_DIR', r"C:\\autoapply\\chrome_profile2")
LOCATION = os.getenv('LOCATION','Bangalore')

JOB_KEYWORDS = [
    'Frontend Developer','React Developer','MERN Developer','Junior Developer',
    'Entry Level','Html Css Developer','Python Developer','Software Engineer',
    'Web Developer intern','Full Stack Intern','Software Engineer Fresher','Junior Web Developer'
]
MAX_APPLIES = int(os.getenv('MAX_APPLIES', '3'))
WAIT_SHORT = 1.0
WAIT_LONG = 3.0

def open_driver():
    from selenium.webdriver.chrome.options import Options
    options = Options()
    options.add_argument(f"--user-data-dir={CHROME_PROFILE_DIR}")
    options.add_argument("--start-maximized")
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
            if applied >= MAX_APPLIES:
                break
            q = urllib.parse.quote(kw)
            url = f"https://www.indeed.co.in/jobs?q={q}&l={LOCATION}&fromage=14"
            driver.get(url)
            time.sleep(WAIT_LONG)
            print('Searching Indeed for:', kw)
            cards = driver.find_elements(By.CSS_SELECTOR, 'div.job_seen_beacon')
            if not cards:
                cards = driver.find_elements(By.CSS_SELECTOR, '.jobsearch-SerpJobCard')
            resume = choose_resume_for_keyword(kw)
            print('Using resume:', resume)
            for card in cards[:5]:
                try:
                    title = card.text.split('\\n')[0][:120]
                except:
                    title = '<no-title>'
                print('Found job:', title)
            print('Indeed done. Applied:', applied)
    finally:
        driver.quit()

if __name__ == '__main__':
    run()
