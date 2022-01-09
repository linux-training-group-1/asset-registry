import os
from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

base_url = os.getenv('STAGING_IP', default='127.0.0.1:5000/')
base_url = "http://" + base_url
username = 'admin'
password = 'password'
service = Service(ChromeDriverManager().install())


def admin_login(driver):
    driver.get(base_url)
    driver.find_element(By.NAME, 'username').send_keys(username)
    driver.find_element(By.NAME, 'password').send_keys(password)
    driver.find_element(By.NAME, 'submit').click()


class TestLogin:
    def test_login_success(self):
        driver = webdriver.Chrome(service=service)
        admin_login(driver)
        assert (base_url + "dashboard") in driver.current_url
        assert "Asset App" in driver.page_source
        assert "Total Assets" in driver.page_source
        driver.quit()

    def test_login_fail(self):
        driver = webdriver.Chrome(service=service)
        driver.get(base_url)
        driver.find_element(By.NAME, 'username').send_keys('john')
        driver.find_element(By.NAME, 'password').send_keys('pass')
        driver.find_element(By.NAME, 'submit').click()
        assert "Incorrect username or password" in driver.page_source
        driver.quit()

    def test_logout_success(self):
        driver = webdriver.Chrome(service=service)
        admin_login(driver)
        driver.get(base_url + 'logout')
        assert "You have been logged out" in driver.page_source
        driver.quit()


class TestListAssets:
    def test_list_assets_success(self):
        driver = webdriver.Chrome(service=service)
        admin_login(driver)
        driver.find_element(By.LINK_TEXT, "LIST ASSETS").click()
        assert (base_url + "list-assets") in driver.current_url
        assert "ID", "Name" in driver.find_element(By.ID, "list-assets-page")
        driver.quit()


class TestAddAssets:
    def test_add_asset_success(self):
        driver = webdriver.Chrome(service=service)
        admin_login(driver)
        driver.find_element(By.LINK_TEXT, "ADD ASSETS").click()
        assert (base_url + "add-asset") in driver.current_url
        driver.find_element(By.NAME, 'assetName').send_keys('Mobile Phone')
        driver.find_element(By.NAME, 'assetOwner').send_keys('John Doe')
        driver.find_element(By.NAME, 'assetDescription').send_keys(
            'Just a Mobile Phone')
        driver.find_element(By.NAME, 'assetLocation').send_keys('Warehouse')
        Select(driver.find_element(By.NAME, 'assetCriticality')
               ).select_by_value('medium')
        driver.find_element(By.NAME, 'submit').click()
        assert (base_url + "list-assets") in driver.current_url
        assert "Mobile Phone", "John Doe" in driver.find_element(
            By.ID, "list-assets-page")
        driver.quit()


class TestEditAssets:
    def test_edit_asset_success(self):
        driver = webdriver.Chrome(service=service)
        admin_login(driver)
        driver.find_element(By.LINK_TEXT, "LIST ASSETS").click()
        driver.find_elements(By.ID, 'edit-asset-btn').pop().click()
        asset_description = driver.find_element(By.NAME, 'assetDescription')
        asset_description.clear()
        asset_description.send_keys('Broken Item')
        driver.find_element(By.NAME, 'submit_update').click()
        assert (base_url + "list-assets") in driver.current_url
        assert "Broken Item" in driver.page_source
        driver.quit()

    def test_delete_asset_success(self):
        driver = webdriver.Chrome(service=service)
        admin_login(driver)
        driver.find_element(By.LINK_TEXT, "LIST ASSETS").click()
        items = driver.find_elements(By.ID, 'edit-asset-btn')
        total_assets = len(items)
        items.pop().click()
        driver.find_element(By.NAME, 'submit_delete').click()
        assert (base_url + "list-assets") in driver.current_url
        assert (total_assets - 1) == len(driver.find_elements(By.ID, "edit-asset-btn"))
        driver.quit()
