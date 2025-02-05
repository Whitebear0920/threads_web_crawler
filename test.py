from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
driver_path = r"E:\CODE\webser\chromedriver-win64\chromedriver-win64/chromedriver.exe"    


service = Service(driver_path)
driver = webdriver.Chrome(service=service)
driver.get('https://www.threads.net/?hl=zh-tw')           
sleep(3)
for i in range(5):
    n = 'window.scrollTo(0, '+str(200+i*2000)+')'
    driver.execute_script(n)
    sleep(1)   
html_content = driver.page_source
soup = BeautifulSoup(html_content, "html.parser")
target_element = soup.select_one(".x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6")
classes = target_element.find_all(class_=["x1a6qonq x6ikm8r x10wlt62 xj0a0fe x126k92a x6prxxf x7r5mf7","xu9jpxn x1n2onr6 xqcsobp x12w9bfk x1wsgiic xuxw1ft x1bl4301"])
for i,j in enumerate(classes):
    print(i," ",j.get_text(strip=True))
##driver.execute_script('window.scrollTo(0, 0)')    
input("按下 Enter 鍵以結束程序並關閉瀏覽器...")
driver.quit()
