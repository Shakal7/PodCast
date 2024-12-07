from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pytest


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

driver.get("http://127.0.0.1:8000/")
driver.maximize_window()

# WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.ID, "username"))
# )
#
# driver.find_element(By.ID, "username").clear()
# driver.find_element(By.ID, "username").send_keys("validuserid")
#
# driver.find_element(By.ID, "password").clear()
# driver.find_element(By.ID, "password").send_keys("validpassword")
#
# driver.find_element(By.NAME, "login").click()


time.sleep(360)
driver.close()


# username_box = driver.find_element(By.ID, "username")
# username_box.send_keys("username")
#
# password_box = driver.find_element(By.ID, "password")
# password_box.send_keys("password")
#
# login_button = driver.find_element(By.ID, "login")
# login_button.click()
#
# assert "home" in driver.page_source
#
# time.sleep(360)
