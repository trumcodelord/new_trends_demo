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

def filter_trends(trend_df, filters):
    filtered_df = trend_df[trend_df["article_count"] >= filters["min_articles"]].copy()

    if filters["search_text"]:
        q = filters["search_text"].lower()
        filtered_df = filtered_df[
            filtered_df["trend_name"].str.lower().str.contains(q, na=False)
            | filtered_df["keywords"].str.lower().str.contains(q, na=False)
        ]

    return filtered_df