import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()


test_episode = ["Episode1", "Episode2", "Third Episode", "Fourth Episode"]


@pytest.mark.parametrize("episode", test_episode)
def test_search_functionality(driver, episode):
    try:
        driver.get("http://127.0.0.1:8000/search")
        print(f"Testing with query: {episode}")

        # Wait for search box to be visible
        search_box = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.NAME, "s"))
        )

        search_box.clear()
        search_box.send_keys(episode)
        time.sleep(3)  # Wait for user to see the text

        search_box.send_keys(Keys.RETURN)

        try:
            # Wait for results
            results = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".search_episodes"))
            )

            if results:  # Check if any results were found
                with open("search_results.txt", "a") as file:
                    file.write(f"Results for {episode}:\n")
                    for result in results:
                        file.write(f"Result: {result.text}\n")
                    file.write("\n" + "-" * 50 + "\n")  # Separator for each episode search result
                print(f"Results for '{episode}' have been written to 'search_results.txt'.")
            else:
                print(f"No results found for '{episode}'.")
                with open("search_results.txt", "a") as file:
                    file.write(f"No results found for {episode}\n")
                    file.write("\n" + "-" * 50 + "\n")  # Separator



        except Exception as e:
            # If there is an error in this block, log the error
            with open("search_results.txt", "a") as file:
                file.write(f"Error for {episode} in search operation: {e}\n")
                file.write("\n" + "-" * 50 + "\n")

        else:
            # If no error occurs in the try block above, log no error message
            with open("search_results.txt", "a") as file:
                file.write(f"No error occurred for {episode}.\n")
                file.write("\n" + "-" * 50 + "\n")  # Separator

    except Exception as e:
        print(f"Error: {e}")
        raise
