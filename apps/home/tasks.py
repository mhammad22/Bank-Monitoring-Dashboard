

from decimal import Decimal
import logging
from selenium.webdriver.support.ui import Select
from apps.home.db import BankTypes, StatusChoices, TransactionTypes
from apps.home.managers import honglelong_extract_num, hongleong_convert_date, may_format_amount, may_format_date, rhb_convert_date, rhb_get_amount_and_type
from core.celery import app
from celery.schedules import crontab
from celery import shared_task
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime, timedelta
from .models import AccountDetails, BankDetails, TaskTime
from selenium.common.exceptions import NoSuchElementException

# Create a logger
logger = logging.getLogger(__name__)

#--------------------------------- MAYBANK ---------------------------------------------

@shared_task(name='home.tasks.fetch_maybank_account_history')
def fetch_maybank_account_history():
    
    print("Fetching data from maybank account")
    
    bank_details = BankDetails.objects.filter(name='MayBank')
    
    for bank in bank_details:
        
        firefox_options = webdriver.FirefoxOptions()

        # set headless mode
        firefox_options.add_argument('--headless')
        firefox_options.add_argument("--disable-infobars")
        firefox_options.set_preference("geo.enabled", False)

        # create Firefox driver instance with the options
        driver = webdriver.Firefox(options=firefox_options)

        username=bank.username
        password=bank.password
        driver.get(bank.url)

        # find username/email field and send the username itself to the input field
        driver.find_element("id", "username").send_keys(username)
        driver.find_element("name", "button").click()
        sleep(10)

        driver.find_element(By.CLASS_NAME, "btn-success").click()
        driver.find_element("id", "my-password-input").send_keys(password)
        driver.find_element(By.CLASS_NAME, "btn-success").click()
        sleep(10)
       
        driver.find_element(By.CLASS_NAME, "panel-body").click()
        sleep(2)
        
        #Saving Account and Account Number
        account_type = driver.find_element(By.XPATH, "//div[1]/div[1]/div/div[2]/div[2]/div[1]/div[2]/div/div[1]/div[1]/div[1]/span[1]").text
        account_number = driver.find_element(By.XPATH, "//div[1]/div[1]/div/div[2]/div[2]/div[1]/div[2]/div/div[1]/div[1]/div[1]/span[3]").text
        
        #select balance related details
        available_balance = driver.find_element(By.XPATH, "(//div[@class='panel-body']/div/div/p[2])").text
        current_balance = driver.find_element(By.XPATH, "((//div[@class='panel-body'])[2]/div[1]/div/span[2])").text
        one_day_float = driver.find_element(By.XPATH, "((//div[@class='panel-body'])[2]/div[2]/div/span[2])").text
        two_day_float = driver.find_element(By.XPATH, "((//div[@class='panel-body'])[2]/div[3]/div/span[2])").text
        last_clearing = driver.find_element(By.XPATH, "((//div[@class='panel-body'])[2]/div[4]/div/span[2])").text
        
        # find all the options in the dropdown
        sleep(5)
        driver.find_element("id", "daysType").click()
        sleep(2)
        # WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID,"daysType"))).click()

        wait = WebDriverWait(driver, 10)
        overlay = wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "LoaderNew---overlay---2UO0j")))
        element = driver.find_element(By.XPATH, "//span[contains(text(), 'Last 60 days')]")
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        element.click()
        
        sleep(10)
        
        #get bank detail object
        bank.current_balance = may_format_amount(current_balance)
        bank.available_balance = may_format_amount(available_balance)
        bank.one_day_float = may_format_amount(one_day_float)
        bank.two_day_float = may_format_amount(two_day_float)
        bank.last_clearing = may_format_amount(last_clearing)
        bank.account_type = BankTypes.CURRENT if 'current' in account_type.lower() else BankTypes.SAVING
        bank.account_num = int(account_number)
        bank.save()

        table_data = driver.find_elements(By.XPATH, '//table/tbody/tr')
        for row in table_data:
            amount = row.find_element(By.XPATH,"./td[4]/div/div/div/span[2]").text
            description = row.find_element(By.XPATH,"./td[2]/span").text
            date = row.find_element(By.XPATH,"./td[1]/span").text
            
            try:
                AccountDetails.objects.create(
                    bank=bank,
                    trans_date=may_format_date(date),
                    description=description,
                    amount = Decimal(amount),
                    trans_type = TransactionTypes.DEBIT,
                    balance = may_format_amount(available_balance),
                    status = StatusChoices.TODO
                )
                
            except Exception as e:
                logger.debug('Account Details Failed to store in DB')

        driver.delete_all_cookies()
        driver.execute_script("window.localStorage.clear()")

        driver.quit()
        print("Done with fetching data from maybank account")

#---------------------------------- RHB -------------------------------------------------
@shared_task(name='home.tasks.fetch_rhb_account_history')
def fetch_rhb_account_history():
    
    print("Fetching Bank details from RHB bank")
    bank = BankDetails.objects.filter(name='RHB').first()
    
    firefox_options = webdriver.FirefoxOptions()

    # set headless mode
    # firefox_options.add_argument('--headless')
    firefox_options.add_argument("--disable-infobars")
    firefox_options.set_preference("geo.enabled", False)

    # create Firefox driver instance with the options
    driver = webdriver.Firefox(options=firefox_options)

    username=bank.username
    password=bank.password
    driver.get(bank.url)

    # find username/email field and send the username itself to the input field
    sleep(10)
    try:
        announcement = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[1]")
    except NoSuchElementException:
        print("Element not found")
        
    if announcement:
        announcement.click()


    # wait for the username field to become visible
    username_field = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div[2]/div/div/form/div[1]/div/div[1]/input'))
    )

    username_field.click()
    username_field.send_keys(username)
    sleep(2)
    login_button_xpath = '/html/body/div[1]/div/div[2]/div[1]/div[2]/div/div/form/div[1]/div/button'
    driver.find_element(By.XPATH, login_button_xpath).click()
    sleep(2)

    captcha_xpath = '/html/body/div[1]/div/div[2]/div[1]/div[2]/div/div/form/div[2]/div/div/div/div/div/div[2]/div[1]'
    driver.find_element(By.XPATH, captcha_xpath).click()
    sleep(2)

    password_xpath = '/html/body/div[1]/div/div[2]/div[1]/div[2]/div/div/form/div[2]/div/div/div/div[2]/div/div[1]/input'
    driver.find_element(By.XPATH, password_xpath).send_keys(password)
    sleep(2)

    login_btn_xpath = '/html/body/div[1]/div/div[2]/div[1]/div[2]/div/div/form/div[2]/div/div/div/div[2]/div/div[3]/button'
    driver.find_element(By.XPATH, login_btn_xpath).click()

    sleep(10)
    account_btn_xpath = '/html/body/div[1]/div/div[1]/div[6]/div/div[2]/div[2]/div[2]/div/div[2]/div/div/ul/li[1]/div/div/div/div'
    account_btn_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, account_btn_xpath)))
    account_btn_field.click()

    sleep(20)
    available_balance_xpath = '/html/body/div[1]/div/div[1]/div[3]/div[2]/div[2]/article/div/div/div[1]/div[2]/div/div/div/div[2]/p[2]'
    available_balance = driver.find_element(By.XPATH, available_balance_xpath).text

    current_balance_xpath = '/html/body/div[1]/div/div[1]/div[3]/div[2]/div[2]/article/div/div/div[1]/div[2]/div/div/div/div[4]/p[2]'
    current_balance = driver.find_element(By.XPATH, current_balance_xpath).text

    view_all_btn_xpath = '/html/body/div[1]/div/div[1]/div[3]/div[2]/div[2]/article/div/div/div[1]/div[3]/div/div[1]/div[2]/div[4]/button'
    view_all_btn = driver.find_element(By.XPATH, view_all_btn_xpath)
    driver.execute_script("arguments[0].scrollIntoView(true);", view_all_btn)
    view_all_btn.click()

    sleep(10)
    all_transactions_xpath = '/html/body/div[1]/div/div[1]/div[3]/div[2]/div[2]/article/div/div/div[1]/div/div[3]/div/div[2]/div/div/div/div/div'
    all_trans = driver.find_elements(By.XPATH, all_transactions_xpath)
    sleep(5)

    for trans in all_trans:
        amount = trans.find_element(By.XPATH, './/div[2]/div[2]/p').text
        description = trans.find_element(By.XPATH, './/div[2]/div/p[1]').text
        date = trans.find_element(By.CLASS_NAME, 'css-1r3d259').text
        
        amt, trans_type = rhb_get_amount_and_type(amount)
        print(amt, trans_type, date, description)
       
        try:
            AccountDetails.objects.create(
                bank=bank,
                trans_date=rhb_convert_date(date),
                description=description,
                amount = Decimal(amt),
                trans_type = TransactionTypes.DEBIT if trans_type == 'debit' else TransactionTypes.CREDIT,
                balance = Decimal(available_balance),
                status = StatusChoices.TODO
            )
            print("Transaction successfully created in the DB")
                    
        except Exception as e:
            logger.debug('Account Details Failed to store in DB')

    driver.delete_all_cookies()
    driver.execute_script("window.localStorage.clear()")

    driver.quit()
    print("Done with fetching data from RHB account")
    
#---------------------------------- HONGLEONG --------------------------------------------
@shared_task(name='home.tasks.fetch_hongleong_account_history')
def fetch_hongleong_account_history():
    firefox_options = webdriver.FirefoxOptions()

    # firefox_options.add_argument('--headless')
    firefox_options.add_argument("--disable-infobars")
    firefox_options.set_preference("geo.enabled", False)

    # create Firefox driver instance with the options
    driver = webdriver.Firefox(options=firefox_options)

    bank = BankDetails.objects.filter(name='HONGLEONG').first()
    username=bank.username
    password=bank.password
    driver.get(bank.url)

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
    account_btn = WebDriverWait(driver, 2).until( EC.visibility_of_element_located((By.XPATH, account_btn_xpath)))
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
        
        if debit:
            is_debit = True
            amount = debit
        else:
            is_debit = False
            amount = credit
            
        print(hongleong_convert_date(date), description, amount, is_debit, honglelong_extract_num(available_balance))
        
        try:
            AccountDetails.objects.create(
                bank=bank,
                trans_date=hongleong_convert_date(date),
                description=description,
                amount = Decimal(amount),
                trans_type = TransactionTypes.DEBIT if is_debit else TransactionTypes.CREDIT,
                balance = Decimal(honglelong_extract_num(available_balance)),
                status = StatusChoices.TODO
            )
            print("Transaction successfully created of hongleong in the DB")

        except Exception as e:
            logger.debug('Account Details of Hoongleong Failed to store in DB')

    driver.delete_all_cookies()
    driver.execute_script("window.localStorage.clear()")

    driver.quit()
    print("Done with fetching data from HONGLEONG account")
 
#---------------------------------- BSN --------------------------------------------
@shared_task(name='home.tasks.fetch_bsn_account_history')
def fetch_bsn_account_history():
    firefox_options = webdriver.FirefoxOptions()

    # set headless mode
    # firefox_options.add_argument('--headless')

    # create Firefox driver instance with the options
    driver = webdriver.Firefox(options=firefox_options)

    bank = BankDetails.objects.filter(name='HONGLEONG').first()
    username=bank.username
    password=bank.password
    driver.get(bank.url)


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
    available_balance = driver.find_element(By.XPATH, '/html/body/div[5]/div/div/form/table/tbody/tr[4]/td/table/tbody/tr[2]/td[3]').text
    driver.find_element(By.CLASS_NAME, "send-money").click()
    driver.find_element(By.XPATH, "//*[@id='table-org']/tbody/tr[2]/td[2]/a").click()
    driver.find_element("name", "saHistory").click()
    dropdown = Select(driver.find_element(By.ID, "saHistoryRange"))
    dropdown.select_by_value("L2M")
    driver.find_element("name", "saHistorySearch").click()

    rows = driver.find_elements(By.XPATH, '/html/body/div[5]/div/div/form/table/tbody/tr[9]/td/table/tbody/tr')
    rows = rows if len(rows) > 1 else []
    data = []
    
    for row in rows or []:
        is_debit = False
        debit = row.find_element(By.XPATH,"./td[3]").text
        credit = row.find_element(By.XPATH,"./td[4]").text
        description = row.find_element(By.XPATH,"./td[2]").text
        date = row.find_element(By.XPATH,"./td[1]").text
        
        if debit:
            is_debit = True
            amount = debit
        else:
            amount = credit
            is_debit = False
        
        try:
            AccountDetails.objects.create(
                bank=bank,
                trans_date=date,
                description=description,
                amount = Decimal(amount),
                trans_type = TransactionTypes.DEBIT if is_debit else TransactionTypes.CREDIT,
                balance = Decimal(available_balance),
                status = StatusChoices.TODO
            )
            print("Transaction successfully created of BSN in the DB")

        except Exception as e:
            logger.debug('Account Details of BSN Failed to store in DB')
        
    print(data)
    driver.quit()
 
 
 
 
 
 
 
 
 
    
app.conf.beat_schedule = {
    # 'maybank': {
    #     'task': 'home.tasks.fetch_maybank_account_history',
    #     'schedule': crontab(minute='*/1')
    #         #crontab(minute='*/' + str(int(TaskTime.objects.all().first().time))),
    #         # timedelta(seconds=int(TaskTime.objects.all().first().time))
    # },
    'rhb': {
        'task': 'home.tasks.fetch_rhb_account_history',
        'schedule': crontab(minute='*/2')
            #crontab(minute='*/' + str(int(TaskTime.objects.all().first().time))),
            # timedelta(seconds=int(TaskTime.objects.all().first().time))
    },
    # 'hongleong': {
    #     'task': 'home.tasks.fetch_hongleong_account_history',
    #     'schedule': crontab(minute='*/2')
    #         #crontab(minute='*/' + str(int(TaskTime.objects.all().first().time))),
    #         # timedelta(seconds=int(TaskTime.objects.all().first().time))
    # },
    # 'bsn': {
    #     'task': 'home.tasks.fetch_bsn_account_history',
    #     'schedule': crontab(minute='*/2')
    #         #crontab(minute='*/' + str(int(TaskTime.objects.all().first().time))),
    #         # timedelta(seconds=int(TaskTime.objects.all().first().time))
    # },
}
