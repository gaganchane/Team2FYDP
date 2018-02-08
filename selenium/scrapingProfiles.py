import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

# https://stackoverflow.com/questions/41502619/mouse-over-operation-in-python-selenium

def startChrome():
    options = Options() 
    options.add_argument("user-data-dir=/Users/sunnygaur/Library/Application Support/Google/Chrome/")
    driver = webdriver.Chrome(chrome_options=options)
    driver.set_page_load_timeout(60)
    return driver

driver = startChrome()
linkedInURL = 'https://www.linkedin.com/'
# driver.get(linkedInURL);

# typeEmail = driver.find_element_by_css_selector(".login-email")
# typePassword = driver.find_element_by_css_selector(".login-password")
# typeEmail.send_keys(TYPE EMAIL)
# typePassword.send_keys(TYPE PASSWORD)
# time.sleep(5)
# typePassword.submit()
# time.sleep(5)

driver.get('https://www.linkedin.com/in/faisale/');
time.sleep(10)

print("searching")
element = driver.find_element_by_css_selector("#ab-indeed-capture a") 
if element.is_displayed():
  print ("Element found")
else:
  print ("Element not found")

print(element.is_enabled())
print(element.is_displayed())
try:
    element.click()
    print("click was attempted")
except WebDriverException:
    print ("Element is not clickable")
element.send_keys(Keys.RETURN)
time.sleep(20)

driver.get('https://www.linkedin.com/in/j2colaco/');
time.sleep(10)

print("searching")
element = driver.find_element_by_css_selector("#ab-indeed-capture a") 
if element.is_displayed():
  print ("Element found")
else:
  print ("Element not found")

print(element.is_enabled())
print(element.is_displayed())
try:
    element.click()
    print("click was attempted")
except WebDriverException:
    print ("Element is not clickable")
element.send_k+eys(Keys.RETURN)
time.sleep(20)

# driver.execute_script()

# print("starting")
# elem = driver.find_element_by_css_selector(".pv-top-card-section__actions--at-bottom span a")
# elem.click()
# elem = driver.find_element_by_css_selector("#ab-indeed-capture a")

# almabase = WebDriverWait(driver, 20).until(
# EC.element_to_be_clickable((By.CSS_SELECTOR, "#ab-indeed-capture")));
# almabase.click()
# print("gotem?")
# almabase = driver.find_element_by_css_selector("#ab-indeed-capture a")
# almabase.click()

# driver.find_element_by_css_selector("#ab-indeed-capture span").click()
# search_box.send_keys('ChromeDriver')
# search_box.submit()
# time.sleep(5) # Let the user actually see something!
# driver.quit()

# driver.get('google.ca')
# driver = webdriver.Chrome()
# Sign into google to access chrome extensions?
# driver.get('https://accounts.google.com/');
# time.sleep(5) # Let the user actually see something!
# gEmail = driver.find_element_by_css_selector("#identifierId")
# gEmail.send_keys(TYPE EMAIL)
# driver.find_element_by_css_selector("#identifierNext").click()
# time.sleep(3)
# gPassword = driver.find_element_by_name("password")
# gPassword.send_keys(TYPE PASSWORD)
# driver.find_element_by_css_selector("#passwordNext").click()
# time.sleep(5)