from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains


navigator_path='/usr/bin/firefox' 

# Initialize Firefox WebDriver with the correct executable path
firefox_options = webdriver.FirefoxOptions()
firefox_options.binary_location = navigator_path

# Pass firefox_options to Firefox WebDriver
driver = webdriver.Firefox( options=firefox_options)


def save_video_from_url(driver,video_url):
    try: 
        driver.get(video_url)
        #_=input("is it ok?")
        video_element = driver.find_element(By.CSS_SELECTOR, "body > video:nth-child(1)")
        # Simulate right-click on the video element
        actions = ActionChains(driver)
        actions.context_click(video_element).perform()
    except: 
        pass


    
    
# Example usage:
while True: 
    link = input("give me the video link \n")
    #name=input("name it \n") 
    link=link.split("range")
    #print(link)
    #print(link[0])
    save_video_from_url(driver, link[0])
    #urllib.request.urlretrieve(link[0], name)
 
    