import streamlit as st
import pandas as pd

def build_article_table(articles):
    rows = []
    for i, article in enumerate(articles, start=1):
        rows.append(
            {
                "STT": i,
                "Tiêu đề": article.get("title", f"Bài viết {i}"),
                "Ngày đăng": article.get("published", ""),
                "Mở bài gốc": article.get("url", ""),
            }
        )
    return pd.DataFrame(rows)

def render_article_table(all_articles, table_height):
    if not all_articles:
        return

    st.markdown(
        '<div class="section-title">Tất cả bài viết trong cụm',
        unsafe_allow_html=True
    
    )

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