from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains


# firefox_options = webdriver.FirefoxOptions()

# # set headless mode
# # firefox_options.add_argument('--headless')

# # create Firefox driver instance with the options
# driver = webdriver.Firefox(options=firefox_options)

from undetected_chromedriver import Chrome, ChromeOptions

# Create ChromeOptions object and add arguments
options = ChromeOptions()
options.headless = False
# options.add_argument("--disable-blink-features=AutomationControlled")

# Set executable path and options for Chrome
driver = Chrome(options=options)

username='Potrait88'
password='Qwer8888@'
driver.get("https://www.mybsn.com.my/mybsn/index.do")


# find username/email field and send the username itself to the input field
driver.find_element("id", "username").send_keys(username)
driver.find_element("name", "confirmImage").click()
sleep(10)

driver.find_element("name", "step2").click()
driver.find_element("id", "password").send_keys(password)
driver.find_element("id", "callEfms").click()

sleep(10)
# Wait for the frame to load and switch to it
frame = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "frame")))
driver.switch_to.frame(frame)

driver.find_element(By.XPATH, "//div[@id='modal-content']/a").click()
driver.find_element(By.CLASS_NAME, "send-money").click()
sleep(2)
#Capture the page source and print it to the console
html = driver.page_source
fileToWrite = open("page_source.html", "w")
fileToWrite.write(html)
fileToWrite.close()

available_balance = driver.find_element(By.XPATH, '/html/body/div[5]/div/div/form/table/tbody/tr[4]/td/table/tbody/tr[2]/td[3]').text
driver.find_element(By.XPATH, "//*[@id='table-org']/tbody/tr[2]/td[2]/a").click()
sleep(2)
driver.find_element("name", "saHistory").click()
sleep(2)
dropdown = Select(driver.find_element(By.ID, "saHistoryRange"))
dropdown.select_by_value("L2M")
driver.find_element("name", "saHistorySearch").click()

rows = driver.find_elements(By.XPATH, '/html/body/div[5]/div/div/form/table/tbody/tr[9]/td/table/tbody/tr')
print("Rows = ", rows)
data = []
if not rows:
    print('No data to fetch ')
else:
    for row in rows:
        debit = row.find_element(By.XPATH,"./td[3]").text
        credit = row.find_element(By.XPATH,"./td[4]").text
        description = row.find_element(By.XPATH,"./td[2]").text
        date = row.find_element(By.XPATH,"./td[1]").text
        data.append([debit, credit, description, date])
    
print(data)
driver.quit()

# Capture the page source and print it to the console
# html = driver.page_source
# fileToWrite = open("page_source.html", "w")
# fileToWrite.write(html)
# fileToWrite.close()

# driver.quit()

