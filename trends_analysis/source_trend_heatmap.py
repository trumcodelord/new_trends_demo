import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np

def build_heatmap_df(trends, trend_df, top_cluster):
    heatmap_rows = []

    for trend in trends:
        for article in trend["articles"]:
            heatmap_rows.append({
                "cluster_id": trend["cluster_id"],
                "source": article.get("source", "Unknown")
            })

    heatmap_df = pd.pivot_table(
        pd.DataFrame(heatmap_rows),
        index="cluster_id",
        columns="source",
        aggfunc="size",
        fill_value=0
    )

    cluster_to_short_name = (
        trend_df.set_index("cluster_id")["shorten_trend_name"]
        .to_dict()
    )

    cluster_order = (
        trend_df
        .sort_values("article_count", ascending=False)
        ["cluster_id"]
        .head(top_cluster)
    )

    heatmap_df = heatmap_df.reindex(
        cluster_order,
        fill_value=0
    )

    heatmap_df.index = [
        cluster_to_short_name[c]
        for c in heatmap_df.index
    ]

    return heatmap_df

def plot_source_trend_heatmap(trends, trend_df, filters, heatmap_height):
    st.markdown(
        '<div class="section-title">Biểu đồ Heatmap các cụm xu hướng</div>',
        unsafe_allow_html=True,
    )

    heatmap_df = build_heatmap_df(
        trends,
        trend_df,
        filters["top_n"]
    )

    short_to_full = (
        trend_df.set_index("shorten_trend_name")["trend_name"]
        .to_dict()
    )

    customdata = np.empty(heatmap_df.shape, dtype=object)

    for i, short_name in enumerate(heatmap_df.index):
        customdata[i, :] = short_to_full.get(short_name, short_name)

    fig = px.imshow(
        heatmap_df,
        color_continuous_scale="Blues",
        aspect="auto",
        labels={
            "x": "Nguồn",
            "y": "Tên xu hướng",
            "color": "Số bài viết"
        }
    )

    fig.update_layout(
        height=heatmap_height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,.35)",
        font=dict(color="#E5E7EB"),
    )

    fig.update_traces(
        customdata=customdata,
        hovertemplate=
        "<b>Xu hướng:</b> %{customdata}<br>"
        "<b>Nguồn báo:</b> %{x}<br>"
        "<b>Số bài báo:</b> %{z}<extra></extra>"
    )

    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})