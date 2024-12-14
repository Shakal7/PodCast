import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.maximize_window()
    yield driver
    driver.quit()


test_data = [
    ("Neel", "neel@example.com", "neel777", "neel777", True, True),
    ("Nituya", "nithu@example.com", "nithu23", "nithu23", True, True),
    ("Bibha", "bihba@example.com", "rbiva123", "rbiva123", True, True),
    ("testuser2", "test2@example.com", "password123", "password123", False, True),
    ("Ontora", "ontora@example.com", "ontora77", "ontora77", True, True),
    # ("duplicate", "biva@example.com", "Duplicate123", "Duplicate123", False, False),
]


@pytest.mark.parametrize("username, email, password, confirm_password, is_premium, expected_result", test_data)
def test_signup(driver, username, email, password, confirm_password, is_premium, expected_result):
    print(f"\nTesting signup for user: {username}")
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

    # Wait for redirection or page result
    try:
        WebDriverWait(driver, 10).until(
            EC.url_contains("/Explore")
        )
        # Check for expected success
        if expected_result:
            print(f"SUCCESS: User '{username}' was successfully signed up and redirected to Explore.")
            assert "Explore" in driver.page_source, f"Failed to confirm Explore page content for: {username}"

        else:
            pytest.fail(f"ERROR: Invalid user '{username}' unexpectedly succeeded in signup.")
    except TimeoutException:
        # Handle failure cases
        print(f"FAILED: User '{username}' was not redirected to Explore page.")
        error_elements = driver.find_elements(By.CLASS_NAME, "error-message")
        if error_elements:
            for error in error_elements:
                print(f"Error Message: {error.text}")
        if expected_result:
            pytest.fail(f"ERROR: Expected signup to succeed for valid user '{username}', but it failed.")
        else:
            print(f"SUCCESS: Signup correctly failed for invalid user '{username}'.")


if __name__ == "__main__":
    pytest.main(["-v", __file__, "--capture=tee-sys"])
