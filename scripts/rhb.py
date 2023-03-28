from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.common.exceptions import NoSuchElementException


chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome('chromedriver', options=chrome_options)

username='Potrait88'
password='Qwer8888@'
driver.get("https://onlinebanking.rhbgroup.com/my/login")

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
available_balance_xpath = '//*[@id="__next"]/div/div[1]/div[3]/div[2]/div[2]/article/div/div/div[1]/div[2]/div/div/div/div[2]/p[2]'
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
print(all_trans)
sleep(5)

print("Available balance = ", available_balance)
print("Current Balalnce = ", current_balance)

for trans in all_trans:
    amount = trans.find_element(By.XPATH, './/div[2]/div[2]/p').text
    print("amount = ", amount)
    description = trans.find_element(By.XPATH, './/div[2]/div/p[1]').text
    print("desc = ", description)
    date = trans.find_element(By.CLASS_NAME, 'css-1r3d259').text
    print("date = ", date)
    
    

# driver.quit()

def get_amount_and_type(amount_string):
    if amount_string.startswith("-"):
        amount = float(amount_string.split()[-1])
        amount_type = "debit"
    else:
        amount = float(amount_string.split()[-1])
        amount_type = "credit"
    return amount, amount_type

def convert_date():
    pass
    # return datetime.strptime(date, '%d %B %Y').date()
