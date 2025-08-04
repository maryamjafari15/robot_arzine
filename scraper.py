import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (TimeoutException , NoSuchElementException , WebDriverException)

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def get_price_by_code(code):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        service = Service()
        driver = webdriver.Chrome(service=service, options=options)
        driver.get("https://www.tgju.org/")

   
        try:
            xpath = f'//tr[@data-market-row="{code}"]/td[1]'
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            price = element.text.strip()
        except (TimeoutException, NoSuchElementException) as e:
            logging.error(f"مشکل در یافتن قیمت : {str(e)}")
            price = "در حال حاضر دریافت قیمت امکان‌پذیر نیست"
        finally:
            driver.quit()
        return price
    
    except WebDriverException as e:
        logging.error(f"خطای WebDriver: {str(e)}")
        return "دریافت قیمت با خطا مواجه شد"
    except Exception as e:
        logging.exception("خطای ناشناخته:")
        return "یک خطای پیش‌بینی‌نشده رخ داد"


