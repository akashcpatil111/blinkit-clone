
import asyncio
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import motor.motor_asyncio
import re

# Database connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.blinkit_commerce

async def seed_products(products):
    if not products:
        print("No products to seed.")
        return
    
    print("Clearing existing products...")
    await db.products.delete_many({})

    print(f"Inserting {len(products)} products into MongoDB...")
    result = await db.products.insert_many(products)
    print(f"Successfully inserted {len(result.inserted_ids)} products.")

def clean_price(price_str):
    if not price_str:
        return 0.0
    # Match any number sequence that might be a price (e.g., "₹ 25", "25", "MRP ₹25")
    # This regex looks for digits possibly with a decimal point
    match = re.search(r"(\d+(\.\d+)?)", price_str.replace(",", ""))
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            return 0.0
    return 0.0

def scrape_blinkit():
    options = Options()
    options.add_argument("--headless=new") 
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    
    scraped_products = []
    
    try:
        print("Navigating to Blinkit...")
        driver.get("https://blinkit.com/")
        
        wait = WebDriverWait(driver, 15)
        
        # 1. Location Handling
        try:
            print("Checking for location modal...")
            asyncio.run(asyncio.sleep(5)) # Wait for any auto-detection
            
            # Strategy: Look for input directly. It is typically present in the modal.
            # Use presence_of_element_located instead of clickable, to avoid obscurity issues.
            try:
                location_input = wait.until(EC.presence_of_element_located((By.NAME, "select-locality")))
                print("Found location input element.")
                
                # Check if visible
                if location_input.is_displayed():
                    print("Input is visible.")
                else:
                    print("Input is NOT visible. Attempting to show it...")
                
                # Use JS to click and focus, to bypass overlays
                driver.execute_script("arguments[0].click();", location_input)
                location_input.clear()
                location_input.send_keys("Gurugram")
                
                asyncio.run(asyncio.sleep(2))
                
                # Look for suggestions
                suggestions = driver.find_elements(By.XPATH, "//div[contains(@class, 'LocationSearchList')]//div")
                print(f"Found {len(suggestions)} suggestions.")
                
                clicked = False
                for s in suggestions:
                    if "Gurugram" in s.text:
                        print(f"Clicking suggestion: {s.text}")
                        s.click()
                        clicked = True
                        break
                
                if not clicked and suggestions:
                    print(f"Clicking first suggestion: {suggestions[0].text}")
                    suggestions[0].click()
                    clicked = True
                
                if not clicked:
                    print("No suggestions clicked. Sending ENTER.")
                    location_input.send_keys(Keys.ENTER)
                    
                asyncio.run(asyncio.sleep(5))

            except Exception as e:
                print(f"Direct input interaction failed: {e}")
                
        except Exception as e:
            print(f"Location handling skipped or failed: {e}")
            with open("debug_fail.html", "w", encoding="utf-8") as f: f.write(driver.page_source)

        # 2. Categories
        # Direct URLs are safest.
        category_urls = [
            ("Dairy & Eggs", "https://blinkit.com/cn/dairy-breakfast/cid/14"),
            ("Fruits & Vegetables", "https://blinkit.com/cn/vegetables-fruits/cid/1487"),
            ("Snacks", "https://blinkit.com/cn/munchies/cid/1253"), 
            ("Beverages", "https://blinkit.com/cn/cold-drinks-juices/cid/339"),
            ("Instant Food", "https://blinkit.com/cn/instant-packaged-food/cid/24")
        ]

        wait = WebDriverWait(driver, 15)

        for cat_name, url in category_urls:
            print(f"Scraping Category: {cat_name} - {url}")
            driver.get(url)
            
            try:
                # Wait for product grid container
                # Trying more generic/robust locators
                wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'Product__ProductContainer')] | //a[contains(@href, '/prn/')]")))
                
                # Scroll to load
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
                asyncio.run(asyncio.sleep(1))
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                asyncio.run(asyncio.sleep(2))

                # Find product cards - often they are anchors or divs wrapping the content
                # Blinkit product cards usually link to a product page
                # Find product cards
                product_cards = driver.find_elements(By.XPATH, "//div[contains(@class, 'Product__UpdatedPlpProductContainer')]")
                
                if not product_cards:
                     # Fallback strategy
                     product_cards = driver.find_elements(By.XPATH, "//div[contains(@class, 'Product__ProductContainer')]")
                
                print(f"Found {len(product_cards)} product cards.")
                
                # Snapshot FIRST CARD for debugging
                if len(product_cards) > 0:
                    try:
                        with open("debug_card.html", "w", encoding="utf-8") as f:
                            f.write(product_cards[0].get_attribute("outerHTML"))
                        print("Dumped first card HTML to debug_card.html")
                    except Exception as e:
                        print(f"Could not dump card HTML: {e}")

                category_count = 0
                for i, card in enumerate(product_cards):
                    if category_count >= 15: 
                        break
                        
                    try:
                        # print(f"DEBUG: Processing card {i}")
                        name = ""
                        price = 0.0
                        image_url = ""
                        quantity = "1 unit"
                        
                        # Name
                        try:
                            # Try 'UpdatedTitle' class
                            name_el = card.find_element(By.XPATH, ".//div[contains(@class, 'Product__UpdatedTitle')]")
                            name = name_el.text.strip()
                            # print(f"DEBUG: Name found: {name}")
                        except Exception as e:
                            # print(f"DEBUG: Name failed for card {i}: {e}")
                            continue # Skip if no name
                            
                        # Price
                        try:
                            price_el = card.find_element(By.XPATH, ".//div[contains(text(), '₹')]")
                            price = clean_price(price_el.text)
                        except Exception as e:
                            # print(f"DEBUG: Price failed: {e}")
                            pass
                            
                        # Image
                        try:
                            img_el = card.find_element(By.TAG_NAME, "img")
                            image_url = img_el.get_attribute("src")
                        except:
                            pass
                            
                        # Quantity
                        try: 
                             qty_el = card.find_element(By.XPATH, ".//span[contains(@class, 'plp-product__quantity')]")
                             quantity = qty_el.text.strip()
                        except:
                             pass

                        description = f"{name} - {quantity}. Sourced from Blinkit."
                        
                        product = {
                            "name": name,
                            "price": price,
                            "category": cat_name,
                            "image_url": image_url,
                            "description": description,
                            "quantity": quantity,
                            "availability": True
                        }
                        
                        # Dedup by name
                        if not any(p['name'] == name for p in scraped_products):
                            scraped_products.append(product)
                            category_count += 1
                            print(f"Extracted: {name} - ₹{price}")

                    except Exception as e:
                        print(f"Error parsing card {i}: {e}")
                        continue
                        
            except Exception as e:
                print(f"Error scraping category {cat_name}: {e}")

        print(f"Total extracted: {len(scraped_products)}")
        return scraped_products
    
    finally:
        driver.quit()

if __name__ == "__main__":
    products = scrape_blinkit()
    if products:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(seed_products(products))
        loop.close()
