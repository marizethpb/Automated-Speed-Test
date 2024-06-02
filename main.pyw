# For automated daily speed test using Netflix's Fast.com, 
# Headless Selenium and Windows Task Scheduler
# is used
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as condition
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import time
import logging
import configparser

# Reading the config file
config_obj = configparser.ConfigParser()
config_obj.read('config.ini')

# Constant in the program setup 
SPEED_TEST_SITE =  config_obj["setup"]["speed_test_site"]# Speed Test site powered by Netflix 
MAXIMUM_WAIT_TIME = config_obj["setup"]["maximum_wait_time"]  # program will wait at most __ seconds for html elements to be clickable
MAXIMUM_SPEED_TEST_RUN = int(config_obj["setup"]["maximum_speed_test_run"])
SPEED_TEST_RESULT_MBPS = config_obj["setup"]["speed_test_result_mbps"]

# XPATH for Website Buttons
SHOW_MORE_INFO_XPATH = config_obj["buttons_xpath"]["show_more_info_xpath"] # Opens to the setting
SETTINGS_XPATH = config_obj["buttons_xpath"]["settings_xpath"] # Where the test duration and parallel connection is modified
SAVE_BUTTON_XPATH = config_obj["buttons_xpath"]["save_button_xpath"] # Save changes to settings

# Constants to be used in filling out the settings
MIN_PARALLEL_CONNECTION_INPUT_XPATH = config_obj["settings_input"]["min_parallel_connection_input_xpath"] 
MIN_PARALLEL_CONNECTION_INPUT = config_obj["settings_input"]["min_parallel_connection_input"] 
MIN_TEST_DURATION_XPATH = config_obj["settings_input"]["min_test_duration_xpath"] 
MIN_TEST_DURATION = config_obj["settings_input"]["min_test_duration"] 
MAX_TEST_DURATION_XPATH  = config_obj["settings_input"]["max_test_duration_xpath"] 
MAX_TEST_DURATION = config_obj["settings_input"]["max_test_duration"] 


def main():
    """ Automates opening of google chrome for continous speed test every 5 minutes. 
    The program covered 24 hours of speed test and is scheduled to run daily 
    to improve internet connection (Speed Tests strengthens internet connection) """
    
    global filelogger, driver, wait

    # File logger
    logging.basicConfig(filename = config_obj["setup"]["log_filename"],level = logging.INFO,
                        format = '%(asctime)s:%(levelname)s:%(name)s:%(message)s')
    filelogger = logging.getLogger()

    # This chunck opens up Google Chrome directed to fast.com in the background
    try: 
        driver = webdriver.Chrome()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
        driver.get(SPEED_TEST_SITE)
        wait = WebDriverWait(driver, MAXIMUM_WAIT_TIME)
        filelogger.info('Chrome opened sucessfully')

    except:
        filelogger.error('Chrome opening encountered an error')

    # This chunck repeats 5 minute-speed test (max time in the settings)
    # for 500 times (Max speed test run) to cover 24-hour speed test
    for _ in range(MAXIMUM_SPEED_TEST_RUN):

        click_an_element(SHOW_MORE_INFO_XPATH, SETTINGS_XPATH)
        filelogger.info(f'[{_} Speed-Test Run] Settings is opened')

        # Parallel Connection is set to 7(min) - 8 (default max) to maximize
        # speed test
        send_keys_to_element((MIN_PARALLEL_CONNECTION_INPUT_XPATH, MIN_PARALLEL_CONNECTION_INPUT),
                             
        # Duration of Speed Test is from 299 to 300 seconds or 5 mins
                            (MIN_TEST_DURATION_XPATH, MIN_TEST_DURATION),
                            (MAX_TEST_DURATION_XPATH, MAX_TEST_DURATION))
        filelogger.info(f'[{_} Speed-Test Run] Settings is modified')

        # Recording the speed test result
        speed_test_result = find_element(SPEED_TEST_RESULT_MBPS)
        filelogger.info(f'[{_} Speed-Test Run] Internet Speed is {speed_test_result.text} MBPS')

        # Save Changes
        click_an_element(SAVE_BUTTON_XPATH)
        filelogger.info(f'[{_} Speed-Test Run] New speed test initatiated')



def find_element(xpath):
    """ Finds an element given the xpath

    Args:
        xpath (str): xpath of the element

    Return: 
        WebElement
    """
    try: 
        driver.find_element(By.XPATH,xpath)
    except TimeoutException:
        filelogger.debug(f"The element of xpath: {xpath} takes too long to be visible / does not exist")

    except: 
        filelogger.error(f"The element of xpath: {xpath} encountered an error (not visible)")

    return driver.find_element(By.XPATH,xpath)


def wait_to_be_clickable(xpath):
    """ Waits for an element to be clickable. Returns WebElement if its clickable

    Args:
        xpath (str): xpath of the element

    Return: 
        WebElement: Clickable WebElement
    """
    try: 
        wait.until(condition.element_to_be_clickable((By.XPATH, xpath)))

    except TimeoutException:
        filelogger.debug(f"The element of xpath: {xpath} takes too long to be clickable / does not exist")

    except: 
        filelogger.error(f"The element of xpath: {xpath} encountered an error (not clickable)")

    return find_element(xpath)


def click_an_element(*xpaths):
    """ Clicks the element/s of the given xpath from left to right

    Args:
        xpath (str): xpath/s of the element to be clicked
    """
    time.sleep(2)
    for xpath in xpaths:

        try:
            button = wait_to_be_clickable(xpath)
            button.click()

        except:
            filelogger.error(f"The element of xpath: {xpath} encountered an error (click didn't work)")


def send_keys_to_element(*xpaths_and_keys_tuple):
    """ Fillout element/s with the key/s provided from order of left to right tuple

    Args:
        xpaths_and_keys_tuple (tuple): element's xpath and key/s in that order
    """
    time.sleep(2)

    # Loops over tuples to fillout xpath with keys 
    for xpath_and_key_tuple in xpaths_and_keys_tuple: 
        min_parallel_input_connection_button = find_element(xpath_and_key_tuple[0])
        min_parallel_input_connection_button.clear()
        min_parallel_input_connection_button.send_keys(xpath_and_key_tuple[1])


main()
