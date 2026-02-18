
import asyncio
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def debug_scrape():
    options = Options()
    options.add_argument("--headless=new") 
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    
    try:
        url = "https://blinkit.com/cn/dairy-breakfast/cid/14"
        print(f"Navigating to {url}...")
        driver.get(url)
        time.sleep(5) # Wait for load

        print("Dumping HTML to debug_page.html...")
        with open("debug_page.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
            
        print("HTML dumped.")
        
        # Quick check for product containers
        containers = driver.find_elements(By.XPATH, "//div[contains(@class, 'Product__ProductContainer')]")
        print(f"Found {len(containers)} containers with primary selector.")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    debug_scrape()
