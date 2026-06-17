import pandas as pd
import plotly.express as px
import streamlit as st
from utils.article import get_article_title, get_article_url, get_article_published

def build_article_table(articles):
    rows = []
    for i, article in enumerate(articles, start=1):
        rows.append(
            {
                "STT": i,
                "Tiêu đề": get_article_title(article, f"Bài viết {i}"),
                "Ngày đăng": get_article_published(article),
                "Mở bài gốc": get_article_url(article),
            }
        )
    return pd.DataFrame(rows)

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

def render_trend_info(selected_trend, selected_rank):
    trend_name = selected_trend.get("trend_name", selected_trend.get("trend", "Xu hướng chưa đặt tên"))
    article_count = selected_trend.get("article_count", selected_trend.get("num_articles", 0))
    cluster_id = selected_trend.get("cluster_id", "")

    d1, d2, d3 = st.columns(3)

    d1.metric("Mã cụm", cluster_id)
    d2.metric("Số bài viết", article_count)
    d3.metric("Xếp hạng", selected_trend.get("rank", selected_rank))

    st.markdown(f"### {trend_name}")

    summary = selected_trend.get("summary", "")
    llm_trend = selected_trend.get("trend", "")

    if summary:
        st.info(summary)
    elif llm_trend:
        st.info(llm_trend)
    else:
        st.warning("Chưa có phần tóm tắt từ mô hình LLM.")

def render_representative_articles(representative_articles):
    if not representative_articles:
        return

    st.markdown("#### Bài viết đại diện")

    st.markdown(
        """
        <div class="demo-hint">
            🔎 <b>Gợi ý demo:</b> bấm vào nút dưới từng bài để mở bài gốc.
            Các bài đại diện giúp chứng minh hệ thống gom theo ngữ nghĩa, không chỉ match từ khóa.
        </div>
        """,
        unsafe_allow_html=True,
    )

    rep_cols = st.columns(min(3, len(representative_articles)))

    for i, article in enumerate(representative_articles[:6], start=1):
        title = get_article_title(article, f"Bài viết {i}")
        url = get_article_url(article)
        published = get_article_published(article)

        with rep_cols[(i - 1) % len(rep_cols)]:
            with st.container(border=True):
                st.markdown("📰")
                st.markdown(f"**{title}**")
                if published:
                    st.caption(published)
                else:
                    st.caption("Bài đại diện")

                if url:
                    st.link_button("🔗 Mở bài gốc", url, use_container_width=True)
                else:
                    st.caption("Không có link bài gốc")

def render_article_table(all_articles, table_height):
    if not all_articles:
        return

    st.markdown("#### Tất cả bài viết trong cụm")

    article_df = build_article_table(all_articles)

    st.dataframe(
        article_df,
        width="stretch",
        hide_index=True,
        height=table_height,
        column_config={
            "STT": st.column_config.NumberColumn("STT", width="small"),
            "Tiêu đề": st.column_config.TextColumn("Tiêu đề", width="large"),
            "Ngày đăng": st.column_config.DatetimeColumn("Ngày đăng", width="medium"),
            "Mở bài gốc": st.column_config.LinkColumn(
                "Mở bài gốc",
                display_text="🔗 Mở bài",
                help="Click để mở bài báo gốc trong tab mới",
                width="small",
            ),
        },
    )

    st.markdown('### Biểu đồ phân bố nguồn bài viết')

    source_df = pd.DataFrame(
        [
            {
                "Nguồn": article.get("source", "Unknown")
            }
            for article in all_articles
        ]
    )

    source_count = (
        source_df
        .value_counts("Nguồn")
        .reset_index(name="Số bài viết")
    )

    fig = px.bar(
        source_count,
        x="Số bài viết",
        y="Nguồn",
        orientation="h",
    )

    fig.update_traces(
        textposition="outside",
        marker_line_width=0,
        hovertemplate="<b>%{y}</b><br>Số bài viết: %{x}<extra></extra>",
        cliponaxis=False,
    )

    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

def render_trend_detail(
    trends,
    filtered_df,
    table_height
):
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