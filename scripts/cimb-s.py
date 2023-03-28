from lib2to3.pgen2.driver import Driver
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from undetected_chromedriver import Chrome, ChromeOptions

# Create ChromeOptions object and add arguments
options = ChromeOptions()
# options.add_argument("--disable-blink-features=AutomationControlled")

# Set executable path and options for Chrome
driver = Chrome(options=options)
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_experimental_option("detach", True)
# driver = webdriver.Chrome('chromedriver', options=chrome_options)

username='Harishop888'
password='Pp889900*'
driver.get("https://www.cimbclicks.com.my/clicks/#/")
sleep(5)
pageSource = driver.page_source
fileToWrite = open("page_source.html", "w")
fileToWrite.write(pageSource)
fileToWrite.close()

driver.find_element("name", "username").send_keys(username)
driver.find_element(By.XPATH, '//*[@id="form-login-step1"]/div[4]/button').click()

sleep(5)
pageSource = driver.page_source

fileToWrite = open("page_source.html", "w")
fileToWrite.write(pageSource)
fileToWrite.close()
driver.find_element(By.CLASS_NAME, 'secure-word-label').click()
# driver.execute_script("arguments[0].scrollIntoView(true);", security_qs)

sleep(2)
driver.find_element(By.NAME, 'password').send_keys(password)
driver.find_element(By.CLASS_NAME, 'btn-login').click()
sleep(50)

# pageSource = driver.page_source

# fileToWrite = open("page_source.html", "w")
# fileToWrite.write(pageSource)
# fileToWrite.close()