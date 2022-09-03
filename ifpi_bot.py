# Imports
import csv
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from loguru import logger

# Globals
main_url = 'https://justnaija.com/music-mp3/'
csv_filename = 'output.csv'


# Function to scrape each listing/item
@logger.catch()
def scrape_data(url):
    logger.info('Opening URL: ' + url)
    driver.get(url)

    wait_by_xpath('//time[@itemprop="dateModified"]', driver, 5)
    date_posted     = driver.find_element(By.XPATH, '//time[@itemprop="dateModified"]').text
    # download_link   = driver.find_element(By.XPATH, '//a[contains(text(),"DOWNLOAD MP3 HERE")]').get_attribute('href')
    download_link   = driver.find_element(By.ID, 'dlf').get_attribute('href')

    post_title_div = driver.find_element(By.XPATH, '//div[@class="mpostheader"]')
    post_title = post_title_div.find_element(By.XPATH, '//span[@class="h1"]').text

    logger.info("Data Scraped")
    logger.info("Post Title" + post_title)
    logger.info("Post URL" + url)
    logger.info("Download link" + download_link)
    logger.info("Date Posted" + date_posted)

    # Push to CSV file
    push_to_csv([post_title, url, download_link, date_posted], csv_filename, 'a')


# Pushing a row to the Output CSV file with Append or Write Mode
@logger.catch()
def push_to_csv(row, filename, write_mode):
    try:
        with open(filename, write_mode, newline='\n') as f_object:
            writer_object = csv.writer(f_object)
            writer_object.writerow(row)
            f_object.close()

        logger.success("Row successfully added to CSV")
    except PermissionError as pe:
        logger.error("CSV Permission Error: " + str(pe))
        logger.error('Please close the output CSV file and re run the bot')
        exit(1)


# Function to navigate through the website
@logger.catch()
def automate():
    logger.info("Opening Website")
    driver.get(main_url)

    wait_by_xpath('//span[@class="pages-info"]', driver, 5)
    total_pages = driver.find_element(By.XPATH, '//span[@class="pages-info"]').text

    total_pages = int(re.search(r'\d+', total_pages).group())

    logger.info("Total Pages: " + str(total_pages))

    # For all pages starting from page # 1
    for page_no in range(1, total_pages+1):
        page_url = main_url + 'page/' + str(page_no) + '/'

        logger.info('Opening URL: ' + page_url)
        driver.get(page_url)

        wait_by_xpath('//h3[@class="file-name myhome"]', driver, 5)
        listings = driver.find_elements(By.XPATH, '//h3[@class="file-name myhome"]')

        logger.info('Total Listings on page # ' + str(page_no) + ': ' + str(len(listings)))

        urls_list = list()
        for listing in listings:
            url = listing.find_element(By.TAG_NAME, 'a').get_attribute('href')
            urls_list.append(url)

        # For all songs/listings on each page
        for url in urls_list:
            try:
                scrape_data(url)
            except NoSuchElementException as e:
                logger.error("Scraping Error: " + e.msg)


# Waiting for an element to appear on the webpage
@logger.catch()
def wait_by_xpath(element_xpath, web_driver, wait_time, cond=ec.presence_of_element_located):
    try:
        WebDriverWait(web_driver, wait_time).until(
            cond((By.XPATH, element_xpath))
        )

        logger.info('Element Found')
        return True
    except TimeoutException:
        logger.error('Timeout Element not found')
        return False


# Function to setup Chrome Driver
@logger.catch()
def setup_chrome():
    # Using Chrome Option, the faster version
    chrome_options = webdriver.ChromeOptions()

    # Disable images in the browser for faster page loading
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    # chrome_options.add_argument("enable-automation")
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--window-size=1920,1080")
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument("--dns-prefetch-disable")
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.setPageLoadStrategy(PageLoadStrategy.NORMAL)
    # chrome_options.page_load_strategy = 'none'
    # chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    # chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    try:
        web_driver = webdriver.Chrome(options=chrome_options)
        logger.success("Chrome Driver is up")
        return web_driver
    except WebDriverException as wde:
        logger.error(wde.msg)
        logger.error('Please download and put ChromeDriver in the project directory or add it in PATH ENV variable')
        exit(1)


# Function to initialize output CSV file with headings
def initialize_csv():
    row = list()
    row.append('Post Title')
    row.append('Post URL')
    row.append('Download URL')
    row.append('Date Posted')
    push_to_csv(row, csv_filename, "w")
    logger.success("CSV Initialized")


# Main Function
if __name__ == '__main__':
    # Setting up Logger
    logger.add("logging/bot_{time}.log", level="TRACE", rotation="100 MB")

    # Initializing the output CSV file
    initialize_csv()

    # Setting up Chrome Driver
    driver = setup_chrome()

    # Automating the website
    automate()

    input('Scraping Finished! Press any key to exit')

    driver.close()
    exit(1)
