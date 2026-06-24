
from underthesea import word_tokenize
from wordcloud import WordCloud
import streamlit as st

def render_trend_wordcloud(all_articles):
    st.markdown(
        '<div class="section-title">Word cloud tiêu đề và mô tả của các bài báo trong xu hướng',
        unsafe_allow_html=True
    )
    texts = []

    for article in all_articles:
        title = article.get("title", "")
        description = article.get("description", "")

        texts.append(
            f"{title} {description}"
        )

    text = "\n".join(texts)
    processed_text = word_tokenize(text, format="text")

    with open("assets/vietnamese-stopwords.txt", "r", encoding="utf-8") as f:
        stopwords = {line.strip() for line in f if line.strip()}

    wc = WordCloud(
        width=1000,
        height=500,
        background_color="white",
        stopwords=stopwords
    ).generate(processed_text)

    st.image(wc.to_array())