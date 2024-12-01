from seleniumbase import SB
from config.env import PROXY_STRING

def launch_browser_with_proxy():
    """
    Launch a SeleniumBase browser in UC mode with optional proxy.
    :param proxy: Proxy string (e.g., "http://user:pass@proxy:port").
    :param headless: Whether to run in headless mode (default: False).
    :param window_size: Browser window size (default: "1200,800").
    """
    try:
        with SB(
            uc=True,  # Enable undetected-chromedriver mode
            headless=False,  # Run in headless mode if True
            incognito=True,  # Enable incognito mode for stealth
            proxy=PROXY_STRING,  # Assign proxy if provided
            window_size="800,800",  # Set the browser window size
        ) as sb:
            # Open Twitter for manual login
            sb.uc_open("https://twitter.com/login")
            print("Browser is ready for manual interaction.")
            print("Proxy:", PROXY_STRING if PROXY_STRING else "No proxy used.")
            
            # Keep the browser open for manual tasks
            input("Press Enter to close the browser...")

    except Exception as e:
        print(f"Error launching browser: {e}")

if __name__ == "__main__":
    launch_browser_with_proxy()
