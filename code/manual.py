from seleniumbase import SB
import sys

def launch_browser_with_proxy(proxy=None):
    try:
        with SB(
            uc=True,  # Enable undetected-chromedriver mode
            headless=False,  # Run in headless mode if True
            incognito=True,  # Enable incognito mode for stealth
            proxy=proxy,  # Assign proxy if provided
            window_size="800,800",  # Set the browser window size
        ) as sb:
            # Open Twitter for manual login
            sb.uc_open("https://x.com/i/flow/login")
            print("Browser is ready for manual interaction.")
            print("Proxy:", proxy if proxy else "No proxy used.")
            
            # Keep the browser open for manual tasks
            input("Press Enter to close the browser...")

    except Exception as e:
        print(f"Error launching browser: {e}")

if __name__ == "__main__":
    # Get the proxy from command line arguments
    proxy = sys.argv[1] if len(sys.argv) > 1 else None
    launch_browser_with_proxy(proxy)
