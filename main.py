from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from urllib import request
import time
import os

chromedriver_autoinstaller.install()
driver = webdriver.Chrome()
driver.get('https://google.com')

serach_word = input("請輸入搜尋圖片：")
print("搜尋", serach_word)
serach_site = driver.find_element(by=By.NAME, value='q')
serach_site.click()
serach_site.send_keys(serach_word)
serach_site.send_keys(Keys.RETURN)
image_button = driver.find_element(by=By.XPATH, value='//*[@id="hdtb-msb"]/div[1]/div/div[2]/a')
image_button.click()

file_count = 1
while True:
    file_name = f'{serach_word}({file_count})'
    if os.path.isdir(file_name):
        file_count += 1
    else:
        os.makedirs(file_name)
        break
print("資料夾名稱", file_name)


img_number_count = 1
error_count = 0
img_xpath_preset = '//*[@id="islrg"]/div[1]/div[imgnumber]/a[1]/div[1]/img'
while True:
    try:
        
        img_xpath = img_xpath_preset.replace('imgnumber', str(img_number_count))
        img_set_xpath = driver.find_element(by=By.XPATH, value=img_xpath)
        img_url = img_set_xpath.get_attribute('src')

        with request.urlopen(img_url) as replay:
            img_data = replay.read()

        with open(f"{file_name}/{serach_word}({img_number_count}).png", "wb") as imgwb:
            imgwb.write(img_data)
        print("下載成功", img_number_count)
        driver.execute_script("arguments[0].scrollIntoView();", img_set_xpath)
        img_number_count += 1
        error_count = 0

    except:
        if error_count >= 50:
            break
        print("下載圖片時發生錯誤", img_number_count)
        error_count += 1
        img_number_count += 1
        time.sleep(1)

driver.quit()