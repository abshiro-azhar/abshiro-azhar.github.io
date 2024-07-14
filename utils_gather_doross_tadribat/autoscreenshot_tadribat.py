from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 
from PIL import Image
from io import BytesIO
import pandas as pd 
import os 


navigator_path='/usr/bin/firefox' 
login_link = 'https://sis.azharegypt.edu.eg/log/regloginstd.php'
question_type={ "t1": [ "اختيار من متعدد" , ""] , "t2": [ "صواب أو خطأ" , "1"], "t3": [ "مــقــالــي" , "2"] }   
 
def take_and_crop_screenshot(driver,css_select,save_name): 
    # Take a screenshot of the entire browser window
    screenshot = driver.get_screenshot_as_png()

    # Use Pillow to open the screenshot image
    img = Image.open(BytesIO(screenshot))
    
    # Get the location and size of the element
    element=driver.find_element(By.CSS_SELECTOR, css_select) 
    location = element.location
    size = element.size

    # Calculate the coordinates for cropping
    left = 4*location['x']
    top = 1.8*location['y']
    right = location['x'] + 1.65*size['width']
    if size['height'] > 650: 
        size['height'] = 650
    bottom = location['y'] + size['height']
    

    # Crop the screenshot to the element
    element_screenshot = img.crop((left, top, right, bottom))

    # Save or display the cropped screenshot
    element_screenshot.save(save_name)
    #element_screenshot.show()


def process(mada,i,tadrib_link,q_key):
    driver.get(tadrib_link)
    # Find the "Images" link and click on it
    box = driver.find_element(By.LINK_TEXT, question_type[q_key][0])
    box.click()
    time.sleep(2)
    #driver.switch_to.frame(1);
    #print(driver.page_source) 
    #answer=driver.find_element(By.PARTIAL_LINK_TEXT, "Sign in")
    #answer.click() 
    q_pref=question_type[q_key][1] 
    popup_css_select=f"#dvPopup{q_pref} > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > iframe:nth-child(1)"
    print( popup_css_select )
    frame = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,popup_css_select)))
    driver.switch_to.frame(frame)
    #while True: 
    driver.find_element(By.CSS_SELECTOR,  '.CollapsiblePanelTab').click()
    time.sleep(2)
    # Get the location and size of the element
    #crop_screenshot(driver,'body > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(1)') 
    #try:  
    css_select_body="body > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(1)"
    i+=1 
    take_and_crop_screenshot(driver,css_select_body, f"{mada}_q{i}.png") 
    print( f"{mada}_q{i}.png")
    try:
        while True:    
            driver.find_element(By.LINK_TEXT,"التالي").click()
            #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,".CollapsiblePanelTab")))
            driver.find_element(By.CSS_SELECTOR,'.CollapsiblePanelTab').click()
            time.sleep(2)
            i+=1
            take_and_crop_screenshot(driver,css_select_body, f"{mada}_q{i}.png") 
            print( f"{mada}_q{i}.png")
    except: 
        print (f"Question type {q_key} finished") 
        #driver.get(tadrib_link)
    return i 


# Initialize Firefox WebDriver with the correct executable path
firefox_options = webdriver.FirefoxOptions()
firefox_options.binary_location = navigator_path

# Pass firefox_options to Firefox WebDriver
driver = webdriver.Firefox( options=firefox_options)


# Open the web page
driver.get(login_link)

# Wait for the page to load
#driver.implicitly_wait(120)
_=input("finish? ") 

subjects=pd.read_csv("mada_link.csv")    # TO fill in 

for mada in subjects:
    if  (mada in ["balaga"]): 
        print(mada)
        end=0
        # cretate obsidian file 
        os.makedirs("./tadribat_md/"+mada,exist_ok=True)
        md_file= "./tadribat_md/"+mada+"/"+mada+".md" 
        pth="./tadribat_md/"+mada
        with open(md_file, 'w') as f:
            # Write the initial content to the file
            #f.write('<div dir="rtl">\n')
            f.write(f'# {mada} \n')
            
        mada_ints = subjects[mada]  
        for m_link in mada_ints:
            
            start=end+1
            if m_link>0: 
                m_link=int(m_link)
                print("Darss " + str(m_link)) 
                
                tadrib_link=f"https://sis.azharegypt.edu.eg/emis/cms/reposid/lcms4/cnt.php?page=p07&&lid={m_link}&cid=107&cnt=268&pageNum_Recordset1=&cors=107"    # TO COMPLEEEEEEEEEEETE 
                for q_key in question_type: 
                    end=process(pth+"/"+mada,end,tadrib_link,q_key)  
                # function to add the lesson in obsidian file
                
                with open(md_file, 'a') as f: 
                    f.write("## درس: \n")
                    f.write("| | | \n")
                    f.write("|--|--|\n")
                    for i in range(start, end , 2): 
                        # you may have to change the name of the screentshot "screenshot%20"
                        f.write(f"|![]({mada}_q{i}.png)| ![]({mada}_q{i+1}.png)|\n") 
                    if (end-start) % 2 == 0: 
                        # you may have to change the name of the screentshot "screenshot%20"
                        f.write(f"|![]({mada}_q{end}.png)| |\n") 
                
        
        
                 
    
