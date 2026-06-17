import pandas as pd
import plotly.express as px
import streamlit as st

from utils.article import get_article_title, get_article_source, get_article_published

def plot_umap(trends, umap_height):
    if not trends or not any("articles" in t and any("umap_x" in a and "umap_y" in a for a in t["articles"]) for t in trends):
        st.warning("Dữ liệu không có thông tin UMAP để hiển thị biểu đồ.")
        return

    umap_df = pd.DataFrame(
        [
            {
                "cluster_id": str(trend.get("cluster_id", "")),
                "title": get_article_title(article, "Bài viết"),
                "source": get_article_source(article),
                "published": get_article_published(article),
                "article_count": int(trend.get("article_count", trend.get("num_articles", 0)) or 0),
                "umap_x": article.get("umap_x"),
                "umap_y": article.get("umap_y"),
            }
            for trend in trends
            for article in trend.get("articles", [])
            if isinstance(article, dict) and "umap_x" in article and "umap_y" in article
        ]
    )

    fig = px.scatter(
        umap_df,
        x="umap_x",
        y="umap_y",
        color="cluster_id",
        color_discrete_sequence=px.colors.qualitative.Alphabet,
        hover_name="title",
        hover_data={
            "source": True,
            "published": True,
            "cluster_id": True,
        },
    )

    fig.update_traces(
        marker=dict(
            size=5,
            opacity=0.7,
            line=dict(width=0),
        )
    )

    fig.update_layout(
        height=umap_height,
        coloraxis_showscale=False,
    )

    fig.update_yaxes(
        scaleanchor="x",
        scaleratio=1,
    )

    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})