import streamlit as st
import pandas as pd
import plotly.express as px

def render_article_timeline_plot(article_df):
    st.markdown(
        '<div class="section-title">Biểu đồ số bài viết theo ngày (timeline)</div>',
        unsafe_allow_html=True
    )

    article_df["Ngày đăng"] = pd.to_datetime(
        article_df["published"],
        utc=True,
        errors="coerce",
    )

    timeline = (
        article_df
        .groupby(
            article_df["Ngày đăng"].dt.date
        )
        .size()
        .reset_index(name="count")
    )

    fig = px.line(
        timeline,
        x="Ngày đăng",
        y="count",
        markers=True,
    )

    fig.update_layout(
        font=dict(color="#E5E7EB"),
        xaxis_title="Ngày",
        yaxis_title="Số bài viết",
    )

    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})