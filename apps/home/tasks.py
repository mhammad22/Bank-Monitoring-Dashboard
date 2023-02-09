

from decimal import Decimal
import logging
from apps.home.db import BankTypes
from core.celery import app
from celery.schedules import crontab
from celery import shared_task
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime
from .models import AccountDetails, BankDetails, TaskTime

# Create a logger
logger = logging.getLogger(__name__)

@shared_task(name='home.tasks.fetch_maybank_account_history')
def fetch_maybank_account_history():
    
    print("Fetching data from maybank account")
    
    bank_details = BankDetails.objects.all()
    
    for bank in bank_details:
        
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_experimental_option("detach", True)
        driver = webdriver.Chrome('chromedriver', options=chrome_options)

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
        
        #get bank detail object
        bank.current_balance = format_amount(current_balance)
        bank.available_balance = format_amount(available_balance)
        bank.one_day_float = format_amount(one_day_float)
        bank.two_day_float = format_amount(two_day_float)
        bank.last_clearing = format_amount(last_clearing)
        bank.account_type = BankTypes.CURRENT if 'current' in account_type.lower() else BankTypes.SAVING
        bank.account_num = int(account_number)
        bank.save()
        

        table_data = driver.find_elements(By.XPATH, '//table/tbody/tr')
        for row in table_data:
            amount = row.find_element(By.XPATH,"./td[4]/div/div/div/span[2]").text
            description = row.find_element(By.XPATH,"./td[3]/div/span[1]").text
            date = row.find_element(By.XPATH,"./td[3]/div/span[2]").text
            
            try:
                AccountDetails.objects.create(
                    bank=bank,
                    date=format_date(date),
                    description=description,
                    amount = Decimal(amount)
                )
                
            except Exception as e:
                logger.debug('Account Details Failed to store in DB')

        driver.quit()
        print("Done with fetching data from maybank account")


def format_date(date):
    return datetime.strptime(date, "%d %b %Y").date()

def format_amount(amount):
    return Decimal(amount.replace('RM', ''))


    
app.conf.beat_schedule = {
    'greetings-task': {
        'task': 'home.tasks.fetch_maybank_account_history',
        'schedule': crontab(minute='*/' + str(int(TaskTime.objects.all().first().time))),
    },
}
