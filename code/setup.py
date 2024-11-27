import os
import site
import shutil
from config.settings import (
    COOKIES_PATH,
    ACCOUNTS_PATH,
    MESSAGE_PATH,
    POST_PATH,
    LOG_PATH,
    QUARANTINE_PATH,
    TWEETS_PATH,
    PICTURES_PATH,
    SUSPENDED_PATH,
    LOGS_PATH,
    BASECASE_PATH
)

def setup_directories_and_files():
    """Sets up required directories and files."""
    print("Setting up directories...")

    # Create directories if they don't exist
    for path in [PICTURES_PATH, COOKIES_PATH, LOGS_PATH]:
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

    print("Setting up config files...")

    # Create files if they don't exist
    for file_path in [
        MESSAGE_PATH, POST_PATH, QUARANTINE_PATH, TWEETS_PATH,
        LOG_PATH, ACCOUNTS_PATH, SUSPENDED_PATH
    ]:
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                pass

def replace_seleniumbase_file():
    """Replaces SeleniumBase's `base_case.py` with the modified version."""
    print("Replacing SeleniumBase's base_case.py...")

    # Locate site-packages directory
    site_packages_path = site.getsitepackages()[0]  # Adjust this for specific environments if needed

    # Target SeleniumBase base_case.py file
    target_file = os.path.join(site_packages_path, "seleniumbase", "fixtures", "base_case.py")

    # Replace the file
    if os.path.exists(target_file):
        try:
            shutil.copy(BASECASE_PATH, target_file)
            print(f"Replaced {target_file} with the modified version.")
        except Exception as e:
            print(f"Failed to replace {target_file}: {e}")
    else:
        print(f"SeleniumBase's base_case.py not found at {target_file}. Skipping replacement.")

def install_dependencies():
    """Install required dependencies."""
    print("Installing dependencies...")
    os.system("pip install -r requirements.txt")
    os.system("python3 -m seleniumwire extractcert")

def setup():
    """Main setup function."""
    setup_directories_and_files()
    install_dependencies()
    replace_seleniumbase_file()
    print("Setup complete.")

def main():
    setup()

if __name__ == '__main__':
    main()
