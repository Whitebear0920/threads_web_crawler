from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from bs4 import BeautifulSoup
import datetime
import firebase_admin
from firebase_admin import credentials, db

# 安裝並啟動 ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 初始化 Firebase
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://webser2025-default-rtdb.asia-southeast1.firebasedatabase.app/'  # 注意最後的斜線
})

#建立今天日期
today = datetime.datetime.today().strftime("%Y-%m-%d")
base_ref = db.reference(f"/posts/{today}")

#取得最後一筆資料
last_post = base_ref.order_by_key().limit_to_last(1).get()
if last_post:
    last_index = max([int(key.replace("post_", "")) for key in last_post.keys()])
else:
    last_index = -1
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

for p in post:
    post_id = f"post_{(p['number']+last_index+1):04d}"
    base_ref.child(post_id).set({
        "text": p["text"],
        "imgs": p["imgs"]
    })
input("按下 Enter 鍵以結束程序並關閉瀏覽器...")
driver.quit()

#資料結構
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