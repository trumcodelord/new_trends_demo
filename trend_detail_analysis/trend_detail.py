import streamlit as st

from .trend_info import render_trend_info
from .representative_articles import render_representative_articles
from .article_table import render_article_table
from .trend_source_bar_chart import render_trend_source_bar_chart
from .trend_timeline_plot import render_trend_timeline_plot
from .trend_wordcloud import render_trend_wordcloud

def select_trend(trends, filtered_df):
    trend_options = [
        f"#{row['rank']} - {row['trend_name']} ({row['article_count']} bài viết)"
        for _, row in filtered_df.sort_values("rank").iterrows()
    ]

    selected_option = st.selectbox("Chọn một xu hướng", trend_options)
    selected_rank = int(selected_option.split(" - ")[0].replace("#", ""))

    selected_trend = None

    for trend in trends:
        rank = int(trend.get("rank", trends.index(trend) + 1))

        if rank == selected_rank:
            selected_trend = trend
            break
    return selected_trend, selected_rank


def render_trend_detail(trends, filtered_df, table_height):
    st.markdown(
        '<div class="section-title">Chi tiết xu hướng</div>',
        unsafe_allow_html=True,
    )

    selected_trend, selected_rank = select_trend(trends, filtered_df)
    render_trend_info(selected_trend, selected_rank)

    representative_articles = selected_trend.get("representative_articles", [])
    render_representative_articles(representative_articles)

    all_articles = selected_trend.get("articles", selected_trend.get("all_articles", []))
    render_article_table(all_articles, table_height)
    render_trend_source_bar_chart(all_articles)
    render_trend_timeline_plot(all_articles)
    render_trend_wordcloud(all_articles)