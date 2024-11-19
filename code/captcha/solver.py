from anticaptchaofficial import funcaptchaProxyless
from config.settings import API_KEY, TWITTER_URL, PUBLIC_KEY


def solve_funcaptcha():
    solver = funcaptchaProxyless()
    solver.set_verbose(1)  # Enable verbose mode for debugging
    solver.set_key(API_KEY)  # Anti-Captcha API key
    solver.set_website_url(TWITTER_URL)  # URL of the captcha
    solver.set_website_key(PUBLIC_KEY)  # FunCaptcha public key

    token = solver.solve_and_return_solution()
    if token:
        return token
    else:
        return None
    
