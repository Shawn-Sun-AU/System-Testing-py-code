import os
from uuid import uuid4
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_T002_S1_valid_login():
    driver = webdriver.Chrome()
    try:
        driver.get(
            "https://opencart.abstracta.us/index.php?route=account/login"
        )
        driver.find_element(By.NAME, "email").send_keys(
            os.environ["TEST_EMAIL"]
        )
        driver.find_element(By.NAME, "password").send_keys(
            os.environ["TEST_PASSWORD"]
        )
        driver.find_element(
            By.CSS_SELECTOR, "input[value='Login']"
        ).click()

        WebDriverWait(driver, 15).until(
            EC.url_contains("route=account/account")
        )
        assert "Edit Account" in driver.find_element(
            By.TAG_NAME, "body"
        ).text

        Path("evidence").mkdir(exist_ok=True)
        driver.save_screenshot("evidence/T002_S1_valid_login.png")
    finally:
        driver.quit()

def test_T002_S2_wrong_password():
    driver = webdriver.Chrome()
    try:
        driver.get(
            "https://opencart.abstracta.us/index.php?route=account/login"
        )
        driver.find_element(By.NAME, "email").send_keys(
            os.environ["TEST_EMAIL"]
        )
        driver.find_element(By.NAME, "password").send_keys(
            os.environ["TEST_PASSWORD"] + "_wrong"
        )
        driver.find_element(
            By.CSS_SELECTOR, "input[value='Login']"
        ).click()

        warning = "Warning: No match for E-Mail Address and/or Password."
        WebDriverWait(driver, 15).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "body"), warning)
        )
        assert "route=account/login" in driver.current_url

        Path("evidence").mkdir(exist_ok=True)
        driver.save_screenshot("evidence/T002_S2_wrong_password.png")
    finally:
        driver.quit()

def test_T002_S3_unknown_email():
    driver = webdriver.Chrome()
    try:
        driver.get(
            "https://opencart.abstracta.us/index.php?route=account/login"
        )
        unknown_email = f"unknown.{uuid4().hex[:12]}@example.com"
        driver.find_element(By.NAME, "email").send_keys(unknown_email)
        driver.find_element(By.NAME, "password").send_keys(
            os.environ["TEST_PASSWORD"]
        )
        driver.find_element(
            By.CSS_SELECTOR, "input[value='Login']"
        ).click()

        warning = "Warning: No match for E-Mail Address and/or Password."
        WebDriverWait(driver, 15).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "body"), warning)
        )
        assert "route=account/login" in driver.current_url

        Path("evidence").mkdir(exist_ok=True)
        driver.save_screenshot("evidence/T002_S3_unknown_email.png")
    finally:
        driver.quit()