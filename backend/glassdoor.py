\
# glassdoor.py - simplified wrapper
import os, time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
from utils import choose_resume_for_keyword

load_dotenv()
CHROME_PROFILE_DIR = os.getenv('CHROME_PROFILE_DIR', r"C:\\autoapply\\chrome_profile2")
LOCATION = os.getenv('LOCATION','Bangalore')
JOB_KEYWORDS = ['Frontend Developer','React Developer']
MAX_APPLIES = int(os.getenv('MAX_APPLIES','1'))

def open_driver():
    from selenium.webdriver.chrome.options import Options
    options = Options()
    options.add_argument(f"--user-data-dir={CHROME_PROFILE_DIR}")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def run():
    driver = open_driver()
    try:
        keywords = [os.getenv('JOB_KEYWORD_OVERRIDE')] if os.getenv('JOB_KEYWORD_OVERRIDE') else JOB_KEYWORDS
        for kw in keywords:
            print('Searching Glassdoor for:', kw)
            time.sleep(0.5)
            print('Using resume:', choose_resume_for_keyword(kw))
        print('Glassdoor done.')
    finally:
        driver.quit()

if __name__ == '__main__':
    run()
