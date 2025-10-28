
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time, json
from urllib.parse import urljoin

cfg = json.load(open("config.json"))
BASE = cfg["BASE_URL"]
HEADERS = cfg.get("HEADERS")

def setup_driver(chrome_driver_path=None, headless=False):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    # useful options
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options) if chrome_driver_path else webdriver.Chrome(options=options)
    return driver

def add_to_cart_and_fill(driver, product_url, user_info):
    driver.get(product_url)
    time.sleep(3)
    # Click add to cart (selector varies)
    try:
        add_btn = driver.find_element(By.CSS_SELECTOR, ".btn._prim._md.add-to-cart")  # example
        add_btn.click()
    except Exception as e:
        print("Could not add to cart automatically, please add manually. Err:", e)
        return False

    time.sleep(2)
    # go to cart
    try:
        driver.get(urljoin(BASE, "/cart/"))
        time.sleep(3)
    except:
        pass

    # start checkout - click checkout button if present
    try:
        checkout_btn = driver.find_element(By.CSS_SELECTOR, "a.checkout")
        checkout_btn.click()
    except:
        print("Proceed to checkout manually. Automation reached pause point.")
        return False

    time.sleep(3)
    # Now fill address (example selectors)
    try:
        # fill phone
        phone_input = driver.find_element(By.NAME, "phone")
        phone_input.clear()
        phone_input.send_keys(user_info.get("phone"))
        # fill address lines
        addr = driver.find_element(By.NAME, "address")
        addr.clear()
        addr.send_keys(user_info.get("address"))
    except Exception as e:
        print("Could not auto-fill all details:", e)

    # STOP before payment
    print("Automation paused. Please review cart and complete payment manually.")
    return True

if __name__ == "__main__":
    d = setup_driver()
    user_info = {"phone":"07XXXXXXXX", "address":"Your delivery address"}
    add_to_cart_and_fill(d, "https://www.jumia.co.ke/sample-product-link", user_info)
