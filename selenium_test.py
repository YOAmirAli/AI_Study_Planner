from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def run_test():
    # Setup Chrome WebDriver (Selenium 4 auto-manages the driver)
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True) # Keeps browser open after script finishes
    driver = webdriver.Chrome(options=options)

    try:
        print("Starting Automated Test...")
        # 1. Navigate to the local application
        driver.get("http://localhost:3000/login")
        driver.maximize_window()
        time.sleep(2)

        # 2. Test Login using your credentials
        print("Testing Login...")
        email_field = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
        password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        
        email_field.send_keys("ut165837452@gmail.com") 
        password_field.send_keys("Usman123")   
        
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()

        # 3. Wait for Dashboard to load and navigate to Tasks to verify CRUD Read Operation
        time.sleep(3)
        print("Navigating to Tasks page...")
        driver.get("http://localhost:5173/tasks")
        time.sleep(2)

        print("Test Complete! Browser is open for your screenshot.")

    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    run_test()
