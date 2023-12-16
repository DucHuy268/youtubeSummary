#!/usr/bin/env python
# coding: utf-8


# Now, retrieve the copied text from the clipboard
import clipboard  # Install the clipboard module using 'pip install clipboard'
# Load USERNAME 
import os
from dotenv import load_dotenv
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium_stealth import stealth
from selenium.webdriver.common.keys import Keys

class ChatGPTFree:
    # Class variable
    species = "Canis familiaris"

    # Constructor (initializer) method
    def __init__(self):
        self.username, self.password = self.loadUserInfo()

    # Load user's info
    def loadUserInfo(self):
        """
        Load the information of user as EMAIL and PASSWORD.
        That Should has a .env file.
        """
        # Load environment variables from the .env file
        load_dotenv()

        # Access the variables
        username = os.getenv("EMAIL")
        password = os.getenv("PASSWORD")
        return username, password 

    # Log in ChatGPT
    def logInChatGPT(self):
        # Create Chromeoptions instance
        options = webdriver.ChromeOptions()
        # Adding argument to disable the AutomationControlled flag 
        options.add_argument("--disable-blink-features=AutomationControlled") 
        options.add_argument("start-maximized")
        #options.add_argument("--headless")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)


        # Set up the WebDriver (replace 'path/to/chromedriver' with your actual path)
        driver = webdriver.Chrome(options=options)

        # Changing the property of the navigator value for webdriver to undefined 
        # driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 


        # Open the website with the button you want to click
        driver.get('https://chat.openai.com/')  # Replace with the actual URL


        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )


        try:
            # Find the button by its data-testid attribute
            button = driver.find_element(By.CSS_SELECTOR, '[data-testid="login-button"]')

            # Click on the button
            button.click()

            time.sleep(5)

            # Find the email input field by its name attribute
            email_input = driver.find_element("name", 'username')

            # Clear the existing value in the input field (if any)
            email_input.clear()

            # Enter your email address
            email_input.send_keys(self.username)

            print("Email address entered successfully")

            # Find the "Continue" button by its class attribute
            continue_button = driver.find_element(By.CLASS_NAME, '_button-login-id')

            # Click the "Continue" button to submit the form
            continue_button.click()

            print("Form submitted successfully")

            time.sleep(3)
            # Find the password input field by its password attribute
            pwd_input = driver.find_element("name", 'password')

            # Clear the existing value in the input field (if any)
            pwd_input.clear()

            # Enter your email address
            pwd_input.send_keys(self.password)

            # Find the "Continue" button by its class attribute
            continue_button = driver.find_element(By.CLASS_NAME, '_button-login-password')

            # Click the "Continue" button to submit the form
            continue_button.click()

            print("Form submitted successfully")


        except Exception as e:
            print(f"Error: {e}")

        finally:
            # Close the browser
            time.sleep(3)
        #     driver.quit()
        return driver
        
    # Question request
    def questionRequest(self, question, driver, questionTime):
        # Find the textarea by id
        textarea = driver.find_element(By.ID,"prompt-textarea")

        # Type the location you want to ask about (e.g., "Where is London?")
        textarea.send_keys(question)
        time.sleep(3)
        
        # Simulate pressing the "Enter" key
        textarea.send_keys(Keys.RETURN)

        print("Pressed 'Enter' in the input field")
        
        time.sleep(questionTime)
        # Find the button by its class name
        button = driver.find_element(By.CSS_SELECTOR,'#__next > div.relative.z-0.flex.h-full.w-full.overflow-hidden > div.relative.flex.h-full.max-w-full.flex-1.flex-col.overflow-hidden > main > div.flex.h-full.flex-col > div.flex-1.overflow-hidden > div > div > div > div:nth-child(3) > div > div > div.relative.flex.w-full.flex-col.lg\:w-\[calc\(100\%-115px\)\].agent-turn > div.flex-col.gap-1.md\:gap-3 > div.mt-1.flex.justify-start.gap-3.empty\:hidden > div > button.flex.items-center.gap-1\.5.rounded-md.p-1.pl-0.text-xs.hover\:text-gray-950.dark\:text-gray-400.dark\:hover\:text-gray-200.disabled\:dark\:hover\:text-gray-400.md\:invisible.md\:group-hover\:visible.md\:group-\[\.final-completion\]\:visible')
                                                      #__next > div.relative.z-0.flex.h-full.w-full.overflow-hidden > div.relative.flex.h-full.max-w-full.flex-1.flex-col.overflow-hidden > main > div.flex.h-full.flex-col > div.flex-1.overflow-hidden > div > div > div > div:nth-child(3) > div > div > div.relative.flex.w-full.flex-col.lg\:w-\[calc\(100\%-115px\)\].agent-turn > div.flex-col.gap-1.md\:gap-3 > div.mt-1.flex.justify-start.gap-3.empty\:hidden > div > button.flex.items-center.gap-1\.5.rounded-md.p-1.pl-0.text-xs.hover\:text-gray-950.dark\:text-gray-400.dark\:hover\:text-gray-200.disabled\:dark\:hover\:text-gray-400.md\:invisible.md\:group-hover\:visible.md\:group-\[\.final-completion\]\:visible
        # Click on the button
        button.click()

        time.sleep(questionTime)
        

        copied_text = clipboard.paste()

        # print("Copied text:", copied_text)
        
        return copied_text
    



