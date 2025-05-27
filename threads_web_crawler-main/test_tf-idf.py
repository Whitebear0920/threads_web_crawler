from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from bs4 import BeautifulSoup
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

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
post = list()
for i in classes:
    post.append(i.get_text(strip=True))

# 印出所有爬取到的文章
print("\n📌 爬取到的 Threads 貼文如下：")
for i, content in enumerate(post):
    print(f"No. {i+1}: {content}")

input("✅ 按下 Enter 鍵開始做 TF-IDF 分析...")
# ---------------- TF-IDF 分析 ---------------- #

# jieba 斷詞 + 空格分隔
segmented_posts = [" ".join(jieba.cut(p)) for p in post]

# 建立 TF-IDF 向量器並轉換整體文章
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(segmented_posts)
feature_names = vectorizer.get_feature_names_out()

# 儲存每篇文章的前 5 個關鍵詞（只有詞，不要分數）
corpus_tfidf = []

# 顯示每篇文章的 top 關鍵詞
print("\n🔍 TF-IDF 關鍵詞分析：")
for idx in range(len(post)):
    tfidf_scores = tfidf_matrix[idx].toarray()[0]
    word_scores = list(zip(feature_names, tfidf_scores))
    top_keywords = sorted(word_scores, key=lambda x: x[1], reverse=True)[:5]
    keywords_only = [word for word, score in top_keywords if score > 0]
    corpus_tfidf.append(keywords_only)

    print(f"\n📄 文章 {idx+1}：{post[idx]}")
    print("⭐ 優先關鍵詞：")
    for word, score in top_keywords:
        if score == 0:
            continue
        print(f"  {word}: {score:.4f}")

# 儲存成 pkl
with open("corpus_tfidf.pkl", "wb") as f:
    pickle.dump(corpus_tfidf, f)

# 關閉瀏覽器
input("\n✅ 已儲存 TF-IDF 關鍵詞至 corpus_tfidf.pkl")
driver.quit()