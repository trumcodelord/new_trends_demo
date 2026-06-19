import pandas as pd
import plotly.express as px
import streamlit as st

def build_heatmap_df(trends, trend_df, max_trend_name_length, top_cluster):
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

    cluster_to_name = {
        trend["cluster_id"]: trend["trend_name"][:max_trend_name_length]
        for trend in trends
    }

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

    heatmap_df = heatmap_df.reindex(cluster_order)

    heatmap_df.index = [
        cluster_to_name[c]
        for c in heatmap_df.index
    ]

    return heatmap_df

def plot_heatmap(trends, trend_df, filters, max_trend_name_length, heatmap_height):
    heatmap_df = build_heatmap_df(trends, trend_df, max_trend_name_length, filters["top_n"])

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
        hovertemplate=
        "Trend: %{y}<br>"
        "Source: %{x}<br>"
        "Articles: %{z}<extra></extra>"
    )

    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})