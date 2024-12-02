import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time


@pytest.fixture
def driver():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.maximize_window()
    yield driver
    driver.quit()


# Test data: username, password, expected result
test_data = [
    ("Priom", "Priom", True),  # Valid credentials
    ("Sokal", "sokal", False),  # Invalid credentials
    ("Shakal", "shakal", False),  # Mixed case
    # ("", "validpassword2", False),  # Missing username
    # ("validuserid3", "", False),  # Missing password
]


@pytest.mark.parametrize("username,password,expected_result", test_data)
def test_login(driver, username, password, expected_result):
    # Open the website
    driver.get("http://127.0.0.1:8000/")

    # Wait for the username field to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )

    # Enter username and password
    driver.find_element(By.ID, "username").clear()
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys(password)

    # Click the login button
    driver.find_element(By.NAME, "login").click()

    # Wait for some result to appear
    time.sleep(5)

    # Check the result
    if expected_result:
        assert "home" in driver.page_source, f"Login failed for valid user: {username}"
    else:
        assert "home" not in driver.page_source, f"Unexpected success for invalid user: {username}"
