import logging
from config.settings import LOG_PATH

logging.basicConfig(level=logging.INFO, filename=LOG_PATH, filemode='a',
                    format='%(message)s')

class NoHttpRequestsFilter(logging.Filter):
    def filter(self, record):
        return not ("HTTP Request" in record.getMessage() and "api.telegram.org" in record.getMessage())
    
class NoChromeDriverFilter(logging.Filter):
    def filter(self, record):
        return not ("patching" in record.getMessage())
    
class NoSeleniumFilter(logging.Filter):
    def filter(self, record):
        return not ("Capturing" in record.getMessage())
    
class NoHTTPFilter(logging.Filter):
    def filter(self, record):
        return not ("HTTP" in record.getMessage())

for handler in logging.getLogger().handlers:
    handler.addFilter(NoHttpRequestsFilter())
    handler.addFilter(NoChromeDriverFilter())
    handler.addFilter(NoSeleniumFilter())
    handler.addFilter(NoHTTPFilter())

def log_info(message):
    logging.info(message)

def log_error(message):
    logging.error(message)

def trace_account_status(account, status):
    if status:
        logging.info(f"SUCCESS - {account['username']}")
    else:
        logging.error(f"FAIL - {account['username']}")
    return status

def trace_account_raid(account, num_tweets, num_success):
    if num_success == num_tweets:
        logging.info(f"{account['username']} - {num_success}/{num_tweets} - SUCCESS")
    else:
        logging.error(f"{account['username']} - {num_success}/{num_tweets} - FAIL")