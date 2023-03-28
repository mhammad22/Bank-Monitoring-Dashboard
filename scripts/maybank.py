from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains


# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# # chrome_options.add_argument('--no-sandbox')
# # chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_experimental_option("detach", True)
# driver = webdriver.Chrome('chromedriver', options=chrome_options)

# create FirefoxOptions object
firefox_options = webdriver.FirefoxOptions()

# set headless mode
# firefox_options.add_argument('--headless')

# create Firefox driver instance with the options
driver = webdriver.Firefox(options=firefox_options)

# ,options=chrome_options
# head to github login page

username='Potrait88'
password='Qwer8888@'
driver.get("https://www.maybank2u.com.my/home/m2u/common/login.do?sessionTimeout=true")

#card navigation for looping
card_nav_xpath = '/html/body/div[2]/div/div[1]/div[1]/div[1]/div/div[1]/div[2]/div/div/div/div[2]/div[2]'
account_nav_xpath = '/html/body/div[2]/div/div[1]/div[1]/div[1]/div/div[1]/div[2]/div/div/div/div[2]/div[1]'

# find username/email field and send the username itself to the input field
driver.find_element("id", "username").send_keys(username)
driver.find_element("name", "button").click()
sleep(10)

driver.find_element(By.CLASS_NAME, "btn-success").click()
driver.find_element("id", "my-password-input").send_keys(password)
driver.find_element(By.CLASS_NAME, "btn-success").click()
sleep(10)
count = 1

#find current balance, one-day float, two-day float, last clearing

while True:
    
    if count > 1:
        acc_nav = driver.find_element(By.XPATH, account_nav_xpath).click()
        # driver.execute_script("arguments[0].scrollIntoView(true);", acc_nav)
        sleep(2)
    count = count + 1
    driver.find_element(By.CLASS_NAME, "panel-body").click()
    sleep(2)
    available_balance = driver.find_element(By.XPATH, "(//div[@class='panel-body']/div/div/p[2])").text
    current_balance = driver.find_element(By.XPATH, "((//div[@class='panel-body'])[2]/div[1]/div/span[2])").text
    one_day_float = driver.find_element(By.XPATH, "((//div[@class='panel-body'])[2]/div[2]/div/span[2])").text
    two_day_float = driver.find_element(By.XPATH, "((//div[@class='panel-body'])[2]/div[3]/div/span[2])").text
    last_clearing = driver.find_element(By.XPATH, "((//div[@class='panel-body'])[2]/div[4]/div/span[2])").text

    print("available balance = ", available_balance)
    print("current balance = ", current_balance)
    print("one day float = ", one_day_float)
    print("two day float = ", two_day_float)
    print("last clearing = ", last_clearing)


    # find all the options in the dropdown
    options = driver.find_element("id", "daysType").click()

    # dropdown = driver.find_elements(By.XPATH, "//ul[@aria-labelledby='daysType']/li")
    sleep(5)
    wait = WebDriverWait(driver, 10)
    overlay = wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "LoaderNew---overlay---2UO0j")))
    element = driver.find_element(By.XPATH, "//span[contains(text(), 'Last 60 days')]")
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()
    element.click()

    sleep(10)

    rows =  driver.find_elements(By.XPATH, '//table/tbody/tr')
    data = []
    for row in rows:
        amount = row.find_element(By.XPATH,"./td[4]/div/div/div/span[2]").text
        description = row.find_element(By.XPATH,"./td[2]/span").text
        date = row.find_element(By.XPATH,"./td[1]/span").text
        data.append([amount, description, date])
        
    # driver.delete_all_cookies()
    # driver.execute_script("window.localStorage.clear()")
    # driver.quit()
    print("data =", data)
    
    driver.find_element(By.XPATH, card_nav_xpath).click()
    sleep(10)

    
# pageSource = driver.page_source

# fileToWrite = open("page_source.html", "w")
# fileToWrite.write(pageSource)
# fileToWrite.close()
