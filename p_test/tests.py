import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.maximize_window()
    yield driver
    driver.quit()


test_data = [
    ("Biva", "biva@example.com", "Biva", "Biva", True, True),  # Valid premium user
    ("testuser2", "test2@example.com", "password123", "password123", False, True),  # Valid non-premium user
]


@pytest.mark.parametrize("username, email, password, confirm_password, is_premium, expected_result", test_data)
def test_signup(driver, username, email, password, confirm_password, is_premium, expected_result):
    # Open the signup page
    driver.get("http://127.0.0.1:8000/signUpListener")  # Update URL if different

    # Wait for the signup form to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )

    # Fill in the form fields
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "confirmPassword").send_keys(confirm_password)

    # Submit the form
    driver.find_element(By.NAME, "signup").click()

    # Wait for the page to load after form submission
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
    except Exception as e:
        pytest.fail(f"Page did not load within the timeout: {e}")

    # Debug: Print the page source for analysis
    print("DEBUG: Page source after signup:\n", driver.page_source)

    # Verify the result
    if expected_result:
        assert "Explore" in driver.page_source, f"Signup failed for valid user: {username}"
    else:
        assert "Explore" not in driver.page_source, f"Unexpected success for invalid user: {username}"

    # Optional premium check
    if is_premium:
        assert "Premium User" in driver.page_source, f"Premium status not displayed for: {username}"
