import streamlit as st
import pandas as pd
import plotly.express as px

def render_trend_timeline_plot(all_articles):
    st.markdown(
        '<div class="section-title">Biểu đồ số bài viết theo ngày (timeline)',
        unsafe_allow_html=True
    )

    timeline_df = pd.DataFrame(
        [
            {
                "Ngày đăng": article["published"]
            }
            for article in all_articles if "published" in article
        ]
    )

    timeline_df["Ngày đăng"] = pd.to_datetime(
        timeline_df["Ngày đăng"],
        utc=True,
        errors="coerce",
    )

    timeline = (
        timeline_df
        .groupby(
            timeline_df["Ngày đăng"].dt.date
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