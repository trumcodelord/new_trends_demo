import pandas as pd
import plotly.express as px
import streamlit as st

def build_heatmap_df(article_df):
    heatmap_df = pd.crosstab(
        article_df["topic_vi"],
        article_df["source"]
    )

    heatmap_df = heatmap_df.loc[
        heatmap_df.sum(axis=1).sort_values(
            ascending=False
        ).index
    ]

    heatmap_df = heatmap_df[
        heatmap_df.sum(axis=0)
        .sort_values(ascending=False)
        .index
    ]

    return heatmap_df

def render_source_topic_heatmap(article_df):
    st.markdown(
        '<div class="section-title">Biểu đồ Heatmap chủ đề theo nguồn báo</div>',
        unsafe_allow_html=True,
    )

    heatmap_df = build_heatmap_df(article_df)

    fig = px.imshow(
        heatmap_df,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="Blues"
    )

    fig.update_traces(
        hovertemplate=(
            "<b>Chủ đề:</b> %{y}<br>"
            "<b>Nguồn báo:</b> %{x}<br>"
            "<b>Số bài báo:</b> %{z}"
            "<extra></extra>"
        )
    )

    fig.update_layout(
        xaxis_title="Nguồn báo",
        yaxis_title="Chủ đề"
    )   

    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})