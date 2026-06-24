
from underthesea import word_tokenize
from wordcloud import WordCloud
import streamlit as st
from collections import Counter
import pandas as pd
import plotly.express as px

def render_word_count_bar_plot(processed_text, stopwords, top_n):
    tokens = [
        w
        for w in processed_text.split()
        if w not in stopwords
    ]
    tokens = [
        w
        for w in tokens
        if len(w) > 1
    ]
    counter = Counter(tokens)


    counter_df = (
        pd.DataFrame(
            counter.items(),
            columns=["word", "count"]
        )
        .sort_values("count", ascending=False)
        .head(top_n)
    )

    fig = px.bar(
        counter_df.sort_values("count", ascending=True),
        x="count",
        y="word",
        orientation="h",
        text="count",
        color="count",
        color_continuous_scale="Blues",
    )

    fig.update_traces(
        textposition="outside",
        marker_line_width=0,
        hovertemplate=(
            "<b>Từ:</b> %{y}<br>"
            "<b>Số lần xuất hiện:</b> %{x}<extra></extra>"
        ),
        cliponaxis=False,
    )

    fig.update_layout(
        height=max(360, 38 * len(counter_df) + 90),
        margin=dict(l=12, r=52, t=12, b=28),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,0.22)",
        font=dict(color="#E5E7EB", size=13),
        xaxis=dict(
            title="Số lần xuất hiện",
            gridcolor="rgba(148,163,184,.13)",
            zeroline=False,
        ),
        yaxis=dict(
            title="",
            gridcolor="rgba(148,163,184,.04)",
            automargin=True,
            tickfont=dict(size=12),
        ),
        coloraxis_showscale=False,
        bargap=0.30,
    )

    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

def render_title_wordcloud(filtered_df, stopwords, top_n):
    text = "\n".join(filtered_df["title"].astype(str))
    processed_text = word_tokenize(text, format="text")

    left, right = st.columns(2)

    with left:
        st.markdown(
            '<div class="section-title">Word cloud và phân phối từ trong tiêu đề',
            unsafe_allow_html=True
        )

        wc = WordCloud(
            width=1000,
            height=500,
            background_color="white",
            stopwords=stopwords
        ).generate(processed_text)

        st.image(wc.to_array())

    with right:
        render_word_count_bar_plot(processed_text, stopwords, top_n)

def render_description_wordcloud(filtered_df, stopwords, top_n):
    text = "\n".join(filtered_df["description"].astype(str))
    processed_text = word_tokenize(text, format="text")
    
    left, right = st.columns(2)

    with left:
        st.markdown(
            '<div class="section-title">Word cloud và phân phối từ trong mô tả',
            unsafe_allow_html=True
        )

        wc = WordCloud(
            width=1000,
            height=500,
            background_color="white",
            stopwords=stopwords
        ).generate(processed_text)

        st.image(wc.to_array())

    with right:
        render_word_count_bar_plot(processed_text, stopwords, top_n)