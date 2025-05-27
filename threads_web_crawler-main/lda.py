import pickle
from gensim import corpora, models
import os
import pyLDAvis
import pyLDAvis.gensim_models

# ---------- 使用者可選擇的關鍵詞來源 ---------- #
available_sources = {
    "1": "corpus_tfidf.pkl",
    "2": "corpus_textrank.pkl",
    "3": "corpus_rake.pkl"
}

print("請選擇要載入的關鍵字來源：")
print(" 1. TF-IDF")
print(" 2. TextRank")
print(" 3. RAKE")
choice = input("請輸入數字(1~3)：")

if choice not in available_sources:
    print("❌ 無效的選擇，程式結束")
    exit()

base_dir = os.path.dirname(os.path.abspath(__file__))  # 取得當前檔案所在目錄
file_name = os.path.join(base_dir, available_sources[choice])

if not os.path.exists(file_name):
    print(f"❌ 找不到檔案：{file_name}，請先執行對應的分析程式")
    exit()

# ---------- 載入資料---------- #
with open(file_name, "rb") as f:
    corpus_keywords = pickle.load(f)

print(f"\n✅ 成功載入：{file_name}")
print(f"🔍 資料總篇數：{len(corpus_keywords)}")

# ---------- 建立 LDA 模型 ---------- #
# 建立字典與向量
dictionary = corpora.Dictionary(corpus_keywords)
bow_corpus = [dictionary.doc2bow(text) for text in corpus_keywords]

# 訓練 LDA 模型
lda_model = models.LdaModel(
    corpus=bow_corpus,
    id2word=dictionary,
    num_topics=5,   # 主題數量，可自行調整
    passes=15,      # 訓練輪數
    random_state=42
)

# 顯示主題
print("\n📌 LDA 主題建模結果：\n")
for idx, topic in lda_model.print_topics(num_words=5):
    print(f"🔸 主題 {idx+1}: {topic}")

# ---------- pyLDAvis 主題視覺化 ---------- #
print("\n📊 正在產生互動式主題視覺化圖表...")
vis_data = pyLDAvis.gensim_models.prepare(lda_model, bow_corpus, dictionary)

html_path = os.path.join(base_dir, "lda_visual.html")
pyLDAvis.save_html(vis_data, html_path)
print(f"✅ 主題視覺化已儲存為：{html_path}")
