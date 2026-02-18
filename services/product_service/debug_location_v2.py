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

def debug_location():
    options = Options()
    # options.add_argument("--headless=new") # Comment out to see if it helps locally (but here it's VM)
    options.add_argument("--headless=new") 
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    
    with open("debug_log.txt", "w") as log:
        def log_print(s):
            print(s)
            log.write(s + "\n")
            
        try:
            log_print("Navigating to https://blinkit.com/ ...")
            driver.get("https://blinkit.com/")
            time.sleep(5)
            
            log_print(f"Title: {driver.title}")
            
            # Check for "Detecting your location..."
            if "Detecting your location..." in driver.page_source:
                log_print("FOUND 'Detecting your location...' overlay.")
                
                # Try ESCAPE
                log_print("Sending ESCAPE...")
                webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                time.sleep(2)
                
                if "Detecting your location..." in driver.page_source:
                     log_print("Overlay STILL PRESENT after ESCAPE.")
                else:
                     log_print("Overlay GONE after ESCAPE.")
            else:
                log_print("'Detecting your location...' NOT found.")

            # Check for 'Select Location' button
            try:
                # Try finding by class if text fails, or by text
                btn = driver.find_element(By.XPATH, "//div[contains(text(), 'Select Location')]")
                log_print("FOUND 'Select Location' button (by text).")
                btn.click()
                log_print("Clicked 'Select Location'.")
                time.sleep(2)
            except Exception as e:
                log_print(f"Could not find/click 'Select Location': {e}")
                
            # Check inputs
            log_print("Searching for inputs...")
            inputs = driver.find_elements(By.TAG_NAME, "input")
            log_print(f"Found {len(inputs)} input elements.")
            for i, inp in enumerate(inputs):
                try:
                    log_print(f"Input {i}: placeholder='{inp.get_attribute('placeholder')}', class='{inp.get_attribute('class')}', visible={inp.is_displayed()}")
                except:
                    log_print(f"Input {i}: (stale element)")
                    
            # Dump HTML
            with open("debug_loc_v2.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            log_print("Dumped HTML to debug_loc_v2.html")

        except Exception as e:
            log_print(f"Error: {e}")
        finally:
            driver.quit()

if __name__ == "__main__":
    debug_location()
