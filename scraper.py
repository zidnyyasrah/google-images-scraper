import bs4
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time

# locate the driver 
driver = webdriver.Chrome()

# URL for scraping the data
item = input('what item do you want to scrape? : ')
searchURL = f'https://www.google.com/search?q={item}&sca_esv=580039890&tbm=isch&source=lnms&sa=X&ved'
driver.get(searchURL)

a = input("press any key to start: ")

# Scroll the page all the way up to load the images
driver.execute_script('window.scrollTo(0,0);')

page_html = driver.page_source
pageSoup = bs4.BeautifulSoup(page_html, 'html.parser')
container = pageSoup.findAll('div',{'class':'isv-r PNCib ViTmJb BUooTd'})   

# find the length of images loaded
len_containers = len(container)
print(f'found {len_containers} image containers')


# to skip recommended items that shows every 25 images
for i in range(1,len_containers+1):
    if i % 25 == 0:
        continue

    # open up every image to see the full res version
    preview_xpath = f'//*[@id="islrg"]/div[1]/div[{i}]/a[1]'
    preview_element = driver.find_element(By.XPATH, preview_xpath)
    preview_URL = preview_element.get_attribute('src')

    # clicking through the image container
    driver.find_element(By.XPATH, preview_xpath).click()

    # Using while loop to wait until the preview images transform into full res images
    timeStarted = time.time()
    while True:
        
        full_xpath = '//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]'
        full_element = driver.find_element(By.XPATH, full_xpath)
        full_URL = full_element.get_attribute('src')

        if preview_URL != full_URL:
            break
        else:
            # making a timeout if the full resolution image can't be loaded
            current_time = time.time()
            if current_time - timeStarted > 5:
                print('timeout, will download the low res image.')
                break


