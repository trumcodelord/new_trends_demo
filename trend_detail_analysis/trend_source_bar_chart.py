import streamlit as st
import pandas as pd
import plotly.express as px

def render_trend_source_bar_chart(all_articles):
    st.markdown(
        '<div class="section-title">Biểu đồ phân bố nguồn bài viết',
        unsafe_allow_html=True
    )

    source_df = pd.DataFrame(
        [
            {
                "source": article.get("source", "Unknown")
            }
            for article in all_articles
        ]
    )

    source_count = (
        source_df
        .value_counts("source")
        .reset_index(name="count")
    )

    fig = px.bar(
        source_count,
        x="count",
        y="source",
        labels={
            "source": "Nguồn báo",
            "count": "Số bài viết"
        },
        orientation="h",
    )

    fig.update_traces(
        textposition="outside",
        marker_line_width=0,
        hovertemplate=(
            "<b>Nguồn báo: </b>%{y}<br>"
            "<b>Số bài viết:</b> %{x}<extra></extra>"
        ),
        cliponaxis=False,
    )

    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})