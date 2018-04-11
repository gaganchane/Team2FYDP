import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

def startChrome():
    options = Options() 
    options.add_argument("user-data-dir=/Users/sunnygaur/Library/Application Support/Google/Chrome/")
    driver = webdriver.Chrome(chrome_options=options)
    driver.set_page_load_timeout(60)
    return driver

def readCSVFile(directory):
  graduates = pd.read_csv(directory)
  return graduates

def loadProfile(driver, URL, cssSelector):
  print(URL)
  driver.get(URL)
  time.sleep(10)
  element = driver.find_element_by_css_selector(cssSelector)
  if element.is_displayed():
    print ("Download button found")
  else:
    print ("Download button not found")
  try:
    element.click()
    print("Button clicked, activating Almabase search")
  except WebDriverException:
    print ("Button is not clickable")
  element.send_keys(Keys.RETURN)
  time.sleep(20)

graduates = readCSVFile('chem-2012-input.csv')
driver = startChrome()
downloadButton = "#ab-indeed-capture a"
print(graduates)
# first = graduates['URL'][1]
# print(first)
# print(first.notnull())

for row in graduates['URL']:
  loadProfile(driver, row, downloadButton)

driver.quit()


# typeEmail = driver.find_element_by_css_selector(".login-email")
# typePassword = driver.find_element_by_css_selector(".login-password")
# typeEmail.send_keys(TYPE EMAIL)
# typePassword.send_keys(TYPE PASSWORD)
# time.sleep(5)
# typePassword.submit()
# time.sleep(5)