import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestLogin:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://the-internet.herokuapp.com/login")
        self.wait = WebDriverWait(self.driver, 10)
        yield
        self.driver.quit()

    def test_page_title(self):
        """Check that the page title is correct"""
        assert "The Internet" in self.driver.title

    def test_username_field_exists(self):
        """Check that the username field exists"""
        username = self.driver.find_element(By.ID, "username")
        assert username is not None

    def test_successful_login(self):
        """Log in with the correct credentials"""
        # Enter username
        self.driver.find_element(By.ID, "username").send_keys("tomsmith")

        # Enter password
        self.driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")

        # Click login button
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Wait for success message
        success_msg = self.wait.until(
            EC.presence_of_element_located((By.ID, "flash"))
        )

        assert "You logged into a secure area!" in success_msg.text

    def test_failed_login_invalid_password(self):
        """Verify error message in case of wrong password"""
        # Enter username
        self.driver.find_element(By.ID, "username").send_keys("tomsmith")

        # Enter wrong password
        self.driver.find_element(By.ID, "password").send_keys("WrongPassword")

        # Click login button
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Wait for error message
        error_msg = self.wait.until(
            EC.presence_of_element_located((By.ID, "flash"))
        )

        assert "Your password is invalid!" in error_msg.text