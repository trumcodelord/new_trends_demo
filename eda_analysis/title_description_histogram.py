import plotly.express as px
import streamlit as st

def render_title_metrics(article_df):
    st.markdown(
        '<div class="section-title">Phân tích phân phối số từ của tiêu đề bài báo</div>',
        unsafe_allow_html=True,
    )
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Trung bình",
        f"{article_df['title_word_count'].mean():.1f}"
    )

    col2.metric(
        "Trung vị",
        int(article_df["title_word_count"].median())
    )

    col3.metric(
        "Nhỏ nhất",
        article_df["title_word_count"].min()
    )

    col4.metric(
        "Lớn nhất",
        article_df["title_word_count"].max()
    )

def render_title_histogram(article_df, filtered_df):
    fig = px.histogram(
        filtered_df,
        x="title_word_count",
        nbins=20
    )

    fig.update_layout(
        xaxis_title="Số từ",
        yaxis_title="Số bài báo"
    )

    fig.update_traces(
        hovertemplate=(
            "<b>Khoảng số từ:</b> %{x}<br>"
            "<b>Số bài báo:</b> %{y}"
            "<extra></extra>"
        )
    )

    mean_words = article_df["title_word_count"].mean()

    fig.add_vline(
        x=mean_words,
        line_dash="dash",
        annotation_text=f"Trung bình = {mean_words:.1f}",
        annotation_yshift=-20
    )

    median_words = article_df["title_word_count"].median()

    fig.add_vline(
        x=median_words,
        line_dash="dot",
        annotation_text=f"Trung vị = {median_words:.0f}",
        annotation_yshift=-70
    )

    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

def render_description_metrics(article_df):
    st.markdown(
        '<div class="section-title">Phân tích phân phối số từ của mô tả bài báo</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Trung bình",
        f"{article_df['description_word_count'].mean():.1f}"
    )

    col2.metric(
        "Trung vị",
        int(article_df["description_word_count"].median())
    )

    col3.metric(
        "Nhỏ nhất",
        article_df["description_word_count"].min()
    )

    col4.metric(
        "Lớn nhất",
        article_df["description_word_count"].max()
    )

def render_description_histogram(article_df, filtered_df):
    fig = px.histogram(
        filtered_df,
        x="description_word_count",
        nbins=20
    )

    fig.update_layout(
        xaxis_title="Số từ",
        yaxis_title="Số bài báo"
    )

    fig.update_traces(
        hovertemplate=(
            "<b>Khoảng số từ:</b> %{x}<br>"
            "<b>Số bài báo:</b> %{y}"
            "<extra></extra>"
        )
    )

    mean_words = article_df["description_word_count"].mean()

    fig.add_vline(
        x=mean_words,
        line_dash="dash",
        annotation_text=f"Trung bình = {mean_words:.1f}",
        annotation_yshift=-20
    )

    median_words = article_df["description_word_count"].median()

    fig.add_vline(
        x=median_words,
        line_dash="dot",
        annotation_text=f"Trung vị = {median_words:.0f}",
        annotation_yshift=-70
    )

    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})