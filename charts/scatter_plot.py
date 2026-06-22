import pandas as pd
import plotly.express as px
import streamlit as st


def plot_scatter(trends, scatter_height):
    quality_df = pd.DataFrame(
        [
            {
                "cluster_id": t["cluster_id"],
                "trend_name": t["trend_name"],
                "article_count": t["article_count"],
                "coherence": t["coherence"],
                "rank": t["rank"],
            }
            for t in trends
        ]
    )

    fig = px.scatter(
        quality_df,
        x="article_count",
        y="coherence",
        hover_name="trend_name",
        color="rank",
        labels={
            "article_count": "Số bài viết",
            "coherence": "Độ gắn kết cụm"
        }
    )

    fig.update_coloraxes(
        reversescale=True
    )

    fig.add_hline(
        y=0.8,
        line_dash="dash",
        annotation_text="Good coherence"
    )

    fig.add_vline(
        x=10,
        line_dash="dot",
    )

    fig.update_traces(
        marker=dict(
            size=5,
            opacity=0.7,
            line=dict(width=0),
        )
    )

    fig.update_layout(
        height=scatter_height,
        coloraxis_showscale=False,
    )

    fig.update_xaxes(
        range=[
            0,
            quality_df["article_count"].max() + 2
        ]
    )

    fig.update_yaxes(
        range=[
            quality_df["coherence"].min() - 0.02,
            quality_df["coherence"].max() + 0.02,
        ]
    )

    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})