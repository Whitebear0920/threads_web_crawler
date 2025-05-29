import jieba
import jieba.analyse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from bs4 import BeautifulSoup
import pickle

# 安裝並啟動 ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 開啟 Threads 網站
driver.get('https://www.threads.net/?hl=zh-tw')
sleep(3)

# 模擬滾動頁面
for i in range(5):
    driver.execute_script(f'window.scrollTo(0, {200 + i * 2000})')
    sleep(1)

# 解析 HTML
soup = BeautifulSoup(driver.page_source, "html.parser")

# 嘗試找出 Threads 文章的區塊
try:
    target_element = soup.select_one(".x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6")
    if target_element:
        classes = target_element.find_all(class_=[
            "x1a6qonq x6ikm8r x10wlt62 xj0a0fe x126k92a x6prxxf x7r5mf7",
            "xu9jpxn x1n2onr6 xqcsobp x12w9bfk x1wsgiic xuxw1ft x1bl4301"
        ])
    else:
        classes = []
except Exception as e:
    print("發生錯誤，無法解析 HTML：", e)
    classes = []

# 儲存爬取到的文章內容
post = []
for i in classes:
    # 移除子元素中叫做「翻譯」的內容
    for unwanted in i.find_all(string="翻譯"):
        unwanted.extract()
    text = i.get_text(strip=True)
    if text:
        post.append(text)

# 顯示所有文章
for i, content in enumerate(post):
    print(f"No. {i+1}: {content}")

input("✅ 按下 Enter 鍵開始 textrank 分析")

# 儲存每篇文章的前 5 個關鍵詞（只有詞，不要分數）
corpus_textrank = []
# ➤ 使用 TextRank 提取關鍵字
for i, text in enumerate(post):
    keywords = jieba.analyse.textrank(text, topK=5, withWeight=True)
    print(f"\n🔍 文章 {i+1} 的關鍵字排名（TextRank Top 5）：")
    keywords_only = []
    for word, weight in keywords:
        print(f"{word} ({weight:.4f})")
        keywords_only.append(word)
    corpus_textrank.append(keywords_only)

# 儲存成 pkl
with open("corpus_textrank.pkl", "wb") as f:
    pickle.dump(corpus_textrank, f)
    
input("\n✅ 已儲存 textrank 關鍵詞至 corpus_textrank.pkl")
driver.quit()