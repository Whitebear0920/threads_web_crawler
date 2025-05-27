from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from bs4 import BeautifulSoup
import jieba
from rake_nltk import Rake
import nltk
import pickle

# 下載 Rake 所需資源
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')

# 安裝並啟動 ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 使用 Selenium 內建的方式來自動偵測 ChromeDriver
driver = webdriver.Chrome()

# 開啟 Threads 網站
driver.get('https://www.threads.net/?hl=zh-tw')           
sleep(3)

# 模擬滾動頁面，使更多內容載入
for i in range(5):
    n = f'window.scrollTo(0, {200 + i * 2000})'
    driver.execute_script(n)
    sleep(1)

# 取得 HTML 內容並解析
html_content = driver.page_source
soup = BeautifulSoup(html_content, "html.parser")

# 找出特定的 HTML 元素
target_element = soup.select_one(".x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6")

# 這個 class 可能需要依據 Threads 網站的變更來調整
# 提取特定 class 的內容
try:
    target_element = soup.select_one(".x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6")
    if target_element:
        classes = target_element.find_all(class_=[
            "x1a6qonq x6ikm8r x10wlt62 xj0a0fe x126k92a x6prxxf x7r5mf7",
            "xu9jpxn x1n2onr6 xqcsobp x12w9bfk x1wsgiic xuxw1ft x1bl4301"
        ])
    else:
        classes = []  # 如果找不到目標元素，回傳空列表
except Exception as e:
    print("發生錯誤，無法解析 HTML：", e)
    classes = []

# 儲存爬取到的文章內容
post = [i.get_text(strip=True) for i in classes]

# 印出所有爬取到的文章
for i, text in enumerate(post):
    print(f"No.{i} : {text[:30]}...")

# 讓使用者選擇要查看的文章內容
input("✅ 按下 Enter 鍵開始 rake 分析")

# 初始化 RAKE
rake = Rake()
corpus_rake = []

for idx, text in enumerate(post):
    words = list(jieba.cut(text))
    joined_text = ' '.join(words)
    rake.extract_keywords_from_text(joined_text)
    keywords = [kw for score, kw in rake.get_ranked_phrases_with_scores()[:5]]  # 最多取前5個
    corpus_rake.append(keywords)
    # print(f"第 {idx+1} 篇完成 ✅")
    print(f"👉 第 {idx+1} 篇文章的前五名關鍵字：")
    for keyword in keywords:
        print(f"   - {keyword}")
    print("-" * 40)


# 存成 pkl
with open("corpus_rake.pkl", "wb") as f:
    pickle.dump(corpus_rake, f)

# 關閉瀏覽器
input("\n✅ 已儲存 rake 關鍵詞至 corpus_rake.pkl")
driver.quit()