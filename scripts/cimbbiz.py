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
# options.headless  = True
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Set executable path and options for Chrome
driver = Chrome(options=options, exit_on_failure=False, exit_on_success=False)


# firefox_options = webdriver.FirefoxOptions()

# # set headless mode
# # firefox_options.add_argument('--headless')
# firefox_options.add_argument("--disable-infobars")
# firefox_options.set_preference("geo.enabled", False)

# # create Firefox driver instance with the options
# driver = webdriver.Firefox(options=firefox_options)

company_id='CA00081007'
username='MONATRADING'
password='M4916378w'
acc_number=8604621982
driver.get("https://www.cimb.bizchannel.com.my/corp/common2/login.do?action=loginRequest")
sleep(15)

driver.find_element("name", "corpId").send_keys(company_id)
driver.find_element("name", "userName").send_keys(username)
driver.find_element("id", "nextButton").click()

sleep(5)
driver.find_element("id", "yesButton").click()

sleep(2)
driver.find_element("name", "passwordEncryption").send_keys(password)
driver.find_element("id", "nextButton").click()

sleep(30)
copy_driver = driver
driver.switch_to.default_content()
frame = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "menuFrame")))
driver.switch_to.frame(frame)
account_statement_xpath = '/html/body/table/tbody/tr/td/table/tbody/tr/td/div[2]/div[3]'
acct_statement = driver.find_element(By.XPATH, account_statement_xpath)
acct_statement.click()

while True:
    show_acct_statment_xpath = '/html/body/table/tbody/tr/td/table/tbody/tr/td/div[2]/span[2]/div[2]'
    driver.find_element(By.XPATH, show_acct_statment_xpath).click()
    sleep(2)
    
    driver.switch_to.default_content()
    frame = WebDriverWait(copy_driver, 10).until(EC.presence_of_element_located((By.NAME, "mainFrame")))
    driver.switch_to.frame(frame)
    sleep(2)

    start_date_xpath = '/html/body/form/table[3]/tbody/tr[1]/td[4]/input[4]'
    driver.find_element(By.XPATH, start_date_xpath).clear()
    driver.find_element(By.XPATH, start_date_xpath).send_keys('01/02/2023')
    sleep(2)
    driver.find_element(By.XPATH, '/html/body/div/div[1]/div[2]/a').click()

    acc_number_xpath = '/html/body/form/table[3]/tbody/tr[7]/td[3]/input[1]'
    driver.find_element(By.XPATH, acc_number_xpath).send_keys(acc_number)

    view_btn_xpath = '/html/body/form/table[4]/tbody/tr/td/div/input'
    driver.find_element(By.XPATH, view_btn_xpath).click()

    rows =  driver.find_elements(By.XPATH, '/html/body/form/table[4]/tbody/tr')
    print(rows)
    data = []
    for row in rows[1:-1]:
        trans_id = row.find_element(By.XPATH, './td[1]').text or ''
        trans_date = row.find_element(By.XPATH, './td[2]').text or ''
        sender_name = row.find_element(By.XPATH, './td[3]').text or ''
        cheque_no = row.find_element(By.XPATH, './td[4]').text or ''
        recipient_ref = row.find_element(By.XPATH, './td[5]').text or ''
        other_payment_detail = row.find_element(By.XPATH, './td[6]').text or ''
        remarks = row.find_element(By.XPATH, './td[7]').text or ''
        debit_amt = row.find_element(By.XPATH, './td[8]').text or ''
        credit_amt = row.find_element(By.XPATH, './td[9]').text or ''
        balance  =row.find_element(By.XPATH, './td[10]').text or ''
        description  =row.find_element(By.XPATH, './td[11]').text or ''
        reference_no  =row.find_element(By.XPATH, './td[12]').text or ''
        
        transaction = [trans_id, trans_date, sender_name, cheque_no, recipient_ref, other_payment_detail, remarks, debit_amt, credit_amt, balance, description, reference_no]
        print(transaction)
        data.append(transaction)
        
    print(data)
    pageSource = driver.page_source

    fileToWrite = open("page_source.html", "w")
    fileToWrite.write(pageSource)
    fileToWrite.close()

    driver.switch_to.default_content()
    switch_menu_frame = WebDriverWait(copy_driver, 10).until(EC.presence_of_element_located((By.NAME, "menuFrame")))
    driver.switch_to.frame(switch_menu_frame)

    acc_balance_xpath = '/html/body/table/tbody/tr/td/table/tbody/tr/td/div[2]/span[2]/div[1]/a'
    driver.find_element(By.XPATH, acc_balance_xpath).click()
    sleep(10)  #sleep set by admin panel here



 
