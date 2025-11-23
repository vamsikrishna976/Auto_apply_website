import subprocess, sys, os
ROOT = os.path.dirname(__file__)

def list_supported_sites():
    return ['indeed','naukri','linkedin','glassdoor']

def apply_for_job(site, keyword, location=None, max_applies=1):
    python_exe = sys.executable
    script_map = {
        'indeed': 'indeed.py',
        'naukri': 'naukri.py',
        'linkedin': 'linkedin.py',
        'glassdoor': 'glassdoor.py'
    }
    script = os.path.join(ROOT, script_map[site])
    if not os.path.exists(script):
        raise FileNotFoundError(f'{script} not found')
    env = os.environ.copy()
    env['LOCATION'] = location or env.get('LOCATION', 'Bangalore')
    env['MAX_APPLIES'] = str(max_applies)
    env['JOB_KEYWORD_OVERRIDE'] = keyword or ''
    cmd = [python_exe, script]
    proc = subprocess.Popen(cmd, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, text=True)
    out, err = proc.communicate()
    return {'site': site, 'returncode': proc.returncode, 'stdout': out, 'stderr': err}
