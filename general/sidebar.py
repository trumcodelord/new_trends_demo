import streamlit as st


def render_sidebar(trend_df):

    st.sidebar.markdown("## 🧭 Bộ lọc")

    search_text = st.sidebar.text_input(
        "Tìm kiếm xu hướng / từ khóa",
        placeholder="Ví dụ: AI, World Cup, Trump...",
    )

    max_count = int(trend_df["article_count"].max()) if len(trend_df) else 0

    min_articles = st.sidebar.slider(
        "Số bài viết tối thiểu",
        min_value=0,
        max_value=max_count,
        value=0,
    )

    top_n = st.sidebar.slider(
        "Số lượng xu hướng hiển thị",
        min_value=5,
        max_value=min(22, max(5, len(trend_df))),
        value=min(12, len(trend_df)),
    )

    st.sidebar.markdown("---")
    st.sidebar.caption("Dữ liệu được đọc từ file `trends.json`.")

    return {
        "search_text": search_text,
        "min_articles": min_articles,
        "top_n": top_n,
    }


def filter_trends(trend_df, filters, article_df=None):
    filtered_df = trend_df[trend_df["article_count"] >= filters["min_articles"]].copy()

    search_text = filters.get("search_text")
    if search_text:
        q = search_text.lower().strip()

        mask_trend = (
            filtered_df["trend_name"].fillna("").str.lower().str.contains(q, na=False, regex=False)
            | filtered_df["keywords"].fillna("").str.lower().str.contains(q, na=False, regex=False)
        )

        if article_df is not None and len(article_df):
            title_mask = article_df.get("title", "").fillna("").str.lower().str.contains(q, na=False, regex=False)
            desc_mask = article_df.get("description", "").fillna("").str.lower().str.contains(q, na=False, regex=False)
            content_mask = article_df.get("content", "").fillna("").str.lower().str.contains(q, na=False, regex=False) if "content" in article_df.columns else False

            matched_cluster_ids = article_df[title_mask | desc_mask | content_mask]["cluster_id"].unique()
            mask_article = filtered_df["cluster_id"].isin(matched_cluster_ids)

            filtered_df = filtered_df[mask_trend | mask_article]
        else:
            filtered_df = filtered_df[mask_trend]

    return filtered_df
