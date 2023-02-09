from logging import Logger
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep
from apps.home.models import Banks, AccountDetails



def populate_maybank_data():
    
    print("Hammmad")
    
    bank_detail = Banks.objects.get(name='Maybank')
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome('chromedriver', options=chrome_options)

    # ,options=chrome_options
    # head to github login page

    username ='shift1226'
    password ='Hello5211!'
    driver.get("https://www.maybank2u.com.my/home/m2u/common/login.do?sessionTimeout=true")


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

    table_data = driver.find_elements(By.XPATH, '//table/tbody/tr')
    data = []
    
    for row in table_data:
        columns = row.find_elements(By.XPATH,"//td") # Use dot in the xpath to find elements with in element.
        table_row = []
        for column in columns:
            date = column.text if index == 0 else '1999-12-10'
            amount = column.text if index == 2 else '0'
            description = column.text if index == 1 else 'N/A'
            table_row.append(column.text)
            index = index + 1
        
        AccountDetails.objects.create(bank=bank_detail, date=date, description=description, amount=amount)
        data.append(table_row)
        
    AccountDetails.objects.create(bank=bank_detail, date='1999-12-10', description='N/A', amount=222.0)
    driver.quit()
    
    # print("data =", data)
    # pageSource = driver.page_source

    # fileToWrite = open("page_source.html", "w")
    # fileToWrite.write(pageSource)
    # fileToWrite.close()


