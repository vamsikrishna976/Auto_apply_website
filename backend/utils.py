import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def safe_find(driver, by, selector, timeout=2):
    try:
        return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, selector)))
    except Exception:
        try:
            return driver.find_element(by, selector)
        except Exception:
            return None

def choose_resume_for_keyword(keyword):
    keyword = (keyword or "").lower()
    env = os.environ
    if 'mern' in keyword:
        return env.get('RESUME_MERN') or env.get('RESUME_DEFAULT')
    if 'front' in keyword or 'react' in keyword or 'html' in keyword:
        return env.get('RESUME_FRONTEND') or env.get('RESUME_DEFAULT')
    if 'entry' in keyword or 'junior' in keyword or 'fresher' in keyword:
        return env.get('RESUME_ENTRY') or env.get('RESUME_DEFAULT')
    return env.get('RESUME_DEFAULT')
