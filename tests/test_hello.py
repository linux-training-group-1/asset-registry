def test_hello():
    assert 1 + 1 == 2


def test_hi():
    assert 2 + 2 == 4


import time
from selenium import webdriver


def test_integration_using_selenium():
    driver = webdriver.Chrome()
    driver.get('https://www.google.com/')
    print(driver.title)
    time.sleep(5)
    search_box = driver.find_element_by_name('q')
    search_box.send_keys('ChromeDriver')
    search_box.submit()
    time.sleep(5)
    print(driver.title)
    driver.quit()
