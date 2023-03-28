from datetime import datetime
from turtle import home
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.common.exceptions import NoSuchElementException
import re


def extract_num(text):
    pattern = r"\d+\.\d+"
    match = re.search(pattern, text)
    if match:
        return float(match.group(0))
    else:
        return 0.0
    
def convert_date(date_st):
    return datetime.strptime(date_st, '%d-%b-%Y').date()


firefox_options = webdriver.FirefoxOptions()

# set headless mode
# firefox_options.add_argument('--headless')
firefox_options.add_argument("--disable-infobars")
firefox_options.set_preference("geo.enabled", False)

# create Firefox driver instance with the options
driver = webdriver.Firefox(options=firefox_options)

username='Potrait88'
password='Qwer8888@'
driver.get("https://s.hongleongconnect.my/rib/app/fo/login?t=1")

try:
    close_btn = driver.find_element(By.CLASS_NAME, "simplemodal-close")

except NoSuchElementException:
    print("No element found")
    
if close_btn:
    close_btn.click()
    
#send username and password and security question for login
driver.find_element(By.ID, "idLoginId").send_keys(username)
driver.find_element(By.CLASS_NAME, "ui-button-text").click()
sleep(2)

driver.find_element(By.ID, "idSBCBConfirmPic").click()
sleep(2)

driver.find_element(By.ID, "idPswd").send_keys(password)
driver.find_element(By.CLASS_NAME, "ui-button-text").click()
sleep(2)

#now user logged in
security_qs = 'idSecQAdd'

try:
    driver.find_element(By.ID, security_qs).send_keys(8888)

    next_btn_xpath = '/html/body/div[2]/div[2]/div/span/div/span/div/div/span/form/div/table/tbody/tr[1]/td[3]/button/span'
    driver.find_element(By.XPATH, next_btn_xpath).click()

except NoSuchElementException:
    print("Security Qs Doesn't appear")

sleep(5)

# Wait for the frame to load and switch to it
frame = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "idMainFrame")))
driver.switch_to.frame(frame)

account_btn_xpath = '/html/body/div[3]/div/div/div/form/div[3]/div/div[2]/div/div/table/tbody/tr/td[1]/div/a'
account_btn = WebDriverWait(driver, 2).until(
    EC.visibility_of_element_located((By.XPATH, account_btn_xpath))
)
account_btn.click()

sleep(10)
dropdown_btn_xpath = '/html/body/div[3]/div/div/div/span/div/div/div[2]/form/span[1]/span[1]/span/table/tbody/tr/td[2]/table/tbody/tr/td/div/div[3]'
driver.find_element(By.XPATH, dropdown_btn_xpath).click()

dropdown_last_30_days_xpath = '/html/body/div[12]/div/ul/li[2]'
driver.find_element(By.XPATH, dropdown_last_30_days_xpath).click()
sleep(10)

available_balance_xpath = '/html/body/div[3]/div/div/div/span/div/div/div[2]/form/span[1]/span[1]/div[1]/div/div/table/tbody/tr/td[2]/table/tbody/tr/td[1]'
available_balance = driver.find_element(By.XPATH, available_balance_xpath).text

current_balance_xpath = '/html/body/div[3]/div/div/div/span/div/div/div[2]/form/span[1]/span[1]/div[1]/div/div/table/tbody/tr/td[2]/table/tbody/tr/td[2]'
current_balance = driver.find_element(By.XPATH, current_balance_xpath).text

rows =  driver.find_elements(By.XPATH, '/html/body/div[3]/div/div/div/span/div/div/div[2]/form/span[1]/span[2]/div/div[1]/table/tbody/tr')

data = []
for row in rows:
        reference = row.find_element(By.XPATH, "./td[3]/span").text
        description = row.find_element(By.XPATH,"./td[2]").text
        date = row.find_element(By.XPATH, "./td[1]/label").text
        debit = row.find_element(By.XPATH, "./td[5]").text
        credit = row.find_element(By.XPATH, "./td[6]").text
        data.append([ description, date, reference, debit, credit])

        print(convert_date(date))
        
    # home_btn_xpath = '/html/body/div[3]/div/div/div/span/span/form/div/div/ul/li[1]'
    # driver.find_element(By.XPATH, home_btn_xpath).click()
    # sleep(5)




