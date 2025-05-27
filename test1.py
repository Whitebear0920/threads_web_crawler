import jieba
import jieba.analyse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from bs4 import BeautifulSoup

# 安裝並啟動 ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 開啟 Threads 網站
driver.get('https://www.threads.net/?hl=zh-tw')
sleep(3)

# 模擬滾動頁面
for i in range(2):
    driver.execute_script(f'window.scrollTo(0, {200 + i * 2000})')
    sleep(1)

# 解析 HTML
soup = BeautifulSoup(driver.page_source, "html.parser")

# 嘗試找出 Threads 文章的區塊
try:
    target_element = soup.select_one(".x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6")
    if target_element:
        classes = target_element.find_all(class_=[
            "x1xdureb xkbb5z x13vxnyz"
        ])
    else:
        classes = []
except Exception as e:
    print("發生錯誤，無法解析 HTML：", e)
    classes = []

post = []
for i, block in enumerate(classes):
    post_temp = block.get_text(strip=True)
    found_imgs = block.find_all('img')
    imgs = []
    img_count = 0
    for img in found_imgs:
        alt = img.get("alt")
        if alt:
            img_count += 1
            imgs.append({"img_count":img_count,
                         "alt":alt})
    post.append({"number":i,
                 "text":post_temp,
                 "imgs":imgs})
for i in post:
    print(f"Post{i['number']}：{i['text']}")
    for j in i['imgs']:
        print(f"Post{i['number']}img{j['img_count']}：{j['alt']}")
    print("=="*5)
input("按下 Enter 鍵以結束程序並關閉瀏覽器...")
driver.quit()

"""
post (list)
│
├── [0] dict
│   ├── number: 0
│   ├── text: "文章1的文字"
│   └── imgs (list)
│       ├── [0] dict
│       ├── img_count
│       └── alt
│
├── [1] dict
│
└── ...

"""

"""
# 儲存文章
post = [i.get_text(strip=True) for i in classes]

# 顯示所有文章
for i, content in enumerate(post):
    print(f"No. {i}: {content}")
"""

"""
# 讓使用者選文章
while True:
    try:
        test = int(input("輸入你想要找的文章號碼(輸入 -1 離開) : "))
        if test == -1:
            break
        elif 0 <= test < len(post):
            print(post[test])
            print(list(jieba.cut(post[test])))
        else:
            print("請輸入有效的文章編號！")
    except ValueError:
        print("請輸入數字！")
    except Exception as e:
        print("發生錯誤：", e)

# ➤ 使用 TextRank 提取關鍵字
for i, text in enumerate(post):
    print(f"\n🔍 文章 {i} 的關鍵字排名（TextRank Top 5）：")
    keywords = jieba.analyse.textrank(text, topK=5, withWeight=True)
    for word, weight in keywords:
        print(f"{word} ({weight:.4f})")
"""
input("按下 Enter 鍵以結束程序並關閉瀏覽器...")
driver.quit()