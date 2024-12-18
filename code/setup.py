import os
import shutil
from config.settings import (
    ACCOUNTS_PATH,
    MESSAGE_PATH,
    POST_PATH,
    LOG_PATH,
    TWEETS_PATH,
    PICTURES_PATH,
    LOGS_PATH
)

def setup_directories_and_files():
    """Sets up required directories and files."""
    print("Setting up directories...")

    # Create directories if they don't exist
    for path in [PICTURES_PATH, LOGS_PATH]:
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

    print("Setting up config files...")

    # Create files if they don't exist
    for file_path in [
        MESSAGE_PATH, POST_PATH, TWEETS_PATH,
        LOG_PATH, ACCOUNTS_PATH
    ]:
        if not os.path.exists(file_path):
            # Create an empty json file if not log_path
            if file_path == LOG_PATH:
                with open(file_path, "w") as f:
                    pass
            else:
                with open(file_path, "w") as f:
                    f.write("[]")

def replace_seleniumbase_file(ORIGINAL_BASECASE_PATH, MODIFIED_BASECASE_PATH):
    """Replaces SeleniumBase's `base_case.py` with the modified version."""
    print("Replacing SeleniumBase's base_case.py...")

    # Replace the file
    if os.path.exists(ORIGINAL_BASECASE_PATH):
        try:
            shutil.copy(MODIFIED_BASECASE_PATH, ORIGINAL_BASECASE_PATH)
            print(f"Replaced {ORIGINAL_BASECASE_PATH} with the modified version.")
        except Exception as e:
            print(f"Failed to replace {ORIGINAL_BASECASE_PATH}: {e}")
    else:
        print(f"SeleniumBase's base_case.py not found at {ORIGINAL_BASECASE_PATH}. Skipping replacement.")

def install_dependencies():
    """Install required dependencies."""
    print("Installing dependencies...")
    os.system("pip install -r requirements.txt")
    # Check if there's a need to extract the certificate
    if not os.path.exists("ca.crt"):
        os.system("python3 -m seleniumwire extractcert")

def install_google_chrome():
    """Install Google Chrome."""
    print("Installing Google Chrome...")
    os.system("sudo apt-get install libxss1 libappindicator1 libindicator7")
    os.system("wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb")
    os.system("sudo apt install ./google-chrome*.deb")
    os.system("rm google-chrome*.deb")

def setup():
    """Main setup function."""
    install_dependencies()
    setup_directories_and_files()

    from config.settings import ORIGINAL_BASECASE_PATH, MODIFIED_BASECASE_PATH
    replace_seleniumbase_file(ORIGINAL_BASECASE_PATH, MODIFIED_BASECASE_PATH)
    install_google_chrome()
    print("Setup complete.")

def main():
    setup()

if __name__ == '__main__':
    main()
