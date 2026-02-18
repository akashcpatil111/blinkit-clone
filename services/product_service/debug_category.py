from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import asyncio

def debug_category():
    options = Options()
    options.add_argument("--headless=new") 
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    
    with open("debug_cat_log.txt", "w") as log:
        def log_print(s):
            print(s)
            log.write(s + "\n")
            
        try:
            log_print("Navigating to https://blinkit.com/ ...")
            driver.get("https://blinkit.com/")
            time.sleep(5)
            
            wait = WebDriverWait(driver, 20)
            
            # Location Logic
            try:
                log_print("Attempting location detection...")
                location_input = wait.until(EC.presence_of_element_located((By.NAME, "select-locality")))
                log_print("Found location input element.")
                
                driver.execute_script("arguments[0].click();", location_input)
                location_input.clear()
                location_input.send_keys("Gurugram")
                time.sleep(2)
                
                suggestions = driver.find_elements(By.XPATH, "//div[contains(@class, 'LocationSearchList')]//div")
                log_print(f"Found {len(suggestions)} suggestions.")
                
                clicked = False
                for s in suggestions:
                    if "Gurugram" in s.text:
                        log_print(f"Clicking suggestion: {s.text}")
                        s.click()
                        clicked = True
                        break
                
                if not clicked and suggestions:
                    suggestions[0].click()
                    clicked = True
                
                if not clicked:
                    location_input.send_keys(Keys.ENTER)
                    
                time.sleep(5)
                
            except Exception as e:
                log_print(f"Location handling failed: {e}")

            # Direct Search Logic
            search_url = "https://blinkit.com/s/?q=milk"
            log_print(f"Navigating to search URL: {search_url}")
            driver.get(search_url)
            time.sleep(10)
            
            log_print(f"Title after search: {driver.title}")
            
            # Dump HTML
            with open("debug_search_direct.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            log_print("Dumped HTML to debug_search_direct.html")
            
            # Check for products (updated selector for Tailwind classes)
            log_print("Searching for product cards using Tailwind classes...")
            product_cards = driver.find_elements(By.XPATH, "//div[@role='button' and .//div[contains(@class, 'tw-line-clamp-2')]]")
            log_print(f"Found {len(product_cards)} products with Tailwind selector.")

            for i, card in enumerate(product_cards[:5]):
                try:
                    name = card.find_element(By.XPATH, ".//div[contains(@class, 'tw-line-clamp-2')]").text
                    price = card.find_element(By.XPATH, ".//div[contains(@class, 'tw-font-semibold') and contains(text(), '₹')]").text
                    qty = card.find_element(By.XPATH, ".//div[contains(@class, 'tw-line-clamp-1') and contains(@class, 'tw-text-200')]").text
                    log_print(f"Product {i}: {name} | {qty} | {price}")
                except Exception as e:
                    log_print(f"Error parsing product {i}: {e}")
            
            products_old = driver.find_elements(By.XPATH, "//div[contains(@class, 'Product__ProductContainer')]")
            log_print(f"Found {len(products_old)} products with 'Product__ProductContainer'.")
            
            products_any = driver.find_elements(By.XPATH, "//div[contains(@class, 'Product')]")
            log_print(f"Found {len(products_any)} products with 'Product'.")

        except Exception as e:
            log_print(f"Error: {e}")
        finally:
            driver.quit()

if __name__ == "__main__":
    debug_category()
