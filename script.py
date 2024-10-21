import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config import path_to_chrome
import re


chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = path_to_chrome
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")


def get_price(url, price_class):
    try:
        # Настройка драйвера
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)
        time.sleep(7)

        # Извлечение цены по указанному классу
        price_element = driver.find_element(By.CLASS_NAME, price_class)
        price = price_element.text.strip()
        driver.quit()  # Закрытие драйвера
        print(price)
        return  re.sub(r'[^\d]','', price.replace('\n', ''))
    except Exception as e:
        return f"Ошибка при получении цены: {url.split('.')[1]}"
    
    # Получение и вывод цен
#for url, price_class in products.items():
    #price = get_price(url, price_class)
    #print(f"Цена для {url}: {price}")