import streamlit as st

from .title_description_histogram import render_title_metrics, render_title_histogram, render_description_metrics, render_description_histogram
from .title_description_box_plot import render_title_boxplot, render_description_boxplot
from .title_description_wordcloud import render_title_wordcloud, render_description_wordcloud
from .title_description_scatter_plot import render_title_description_word_count_scatter_plot

def render_eda_analysis(article_df):
    selected_sources = st.multiselect(
        "Nguồn báo",
        sorted(article_df["source"].unique()),
        default=sorted(article_df["source"].unique())
    )

    selected_topics = st.multiselect(
        "Chủ đề",
        sorted(article_df["topic_vi"].unique()),
        default=sorted(article_df["topic_vi"].unique())
    )

    filtered_df = article_df[
        article_df["source"].isin(selected_sources)
        & article_df["topic_vi"].isin(selected_topics)
    ]

    render_title_metrics(article_df)
    render_title_histogram(article_df, filtered_df)

    render_description_metrics(article_df)
    render_description_histogram(article_df, filtered_df)


    render_title_boxplot(filtered_df)
    render_description_boxplot(filtered_df)

    with open("assets/vietnamese-stopwords.txt", "r", encoding="utf-8") as f:
        stopwords = {line.strip() for line in f if line.strip()}

    top_n = st.slider(
       "Top từ khóa",
       1,
       50,
       10
    )

    render_title_wordcloud(filtered_df, stopwords, top_n)
    render_description_wordcloud(filtered_df, stopwords, top_n)

    render_title_description_word_count_scatter_plot(filtered_df)