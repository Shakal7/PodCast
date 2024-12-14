import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
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
    ("Etu", "etu@example.com", "Etu12345", "Etu12345", "Monthly Premium - BDT100", True),  # Valid premium user
    ("testuser", "testuser@example.com", "password123", "password123", "", True),  # Valid listener (normal user)
    ("Mithila", "mithila@example.com", "Mithila123", "Mithila123", "Yearly Premium - BDT1200", True),
    ("Laabanno", "llaabonno@example.com", "labooo111", "labooo111", "Monthly Premium - BDT100", True),
    ("Dristy", "dristyy@example.com", "dristyy23", "dristyy23", "Monthly Premium - BDT100", True),
]


@pytest.mark.parametrize("username, email, password, confirm_password, subscription_plan, expected_result", test_data)
def test_signup(driver, username, email, password, confirm_password, subscription_plan, expected_result):
    print(f"\nTesting signup for user: {username} (Subscription Plan: {subscription_plan})")
    driver.get("http://127.0.0.1:8000/signUpPremium")  # Adjust to your actual URL

    # Wait for the signup form to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )

    # Fill in the form fields
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "confirmPassword").send_keys(confirm_password)

    # Select subscription plan if provided
    if subscription_plan:
        dropdown = Select(driver.find_element(By.NAME, "subscriptionPlan"))
        dropdown.select_by_visible_text(subscription_plan)

    # Submit the form
    driver.find_element(By.NAME, "signup").click()

    try:
        # Wait for redirection to Explore page
        WebDriverWait(driver, 10).until(
            EC.url_contains("/Explore")
        )

        # Confirm successful redirection
        assert "/Explore" in driver.current_url.lower(), f"Expected redirection to '/explore', but got: {driver.current_url}"

        # Check for expected content on the Explore page
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "welcome-message"))  # Replace with actual class name
        )

        if expected_result:
            print(f"SUCCESS: User '{username}' was successfully signed up and redirected to Explore.")
            if subscription_plan:
                assert "Explore!" in driver.page_source, f"Premium message not found for: {username}"
            else:
                assert "Welcome Listener!" in driver.page_source, f"Listener message not found for: {username}"
        else:
            pytest.fail(f"ERROR: Invalid user '{username}' unexpectedly succeeded in signup.")

    except TimeoutException:
        # Log failure details
        print(f"FAILED: User '{username}' was not redirected to Explore page or content not found.")
        error_messages = driver.find_elements(By.CLASS_NAME, "error-message")
        if error_messages:
            for error in error_messages:
                print(f"Error Message: {error.text}")
        if expected_result:
            pytest.fail(f"ERROR: Expected signup to succeed for valid user '{username}', but it failed.")
        else:
            print(f"SUCCESS: Signup correctly failed for invalid user '{username}'.")


if __name__ == "__main__":
    pytest.main(["-v", __file__, "--capture=tee-sys"])
