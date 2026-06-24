import streamlit as st

def render_dataset_metrics(article_df, metrics):
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "📰 Bài viết",
        metrics["total_scraped_articles"]
    )

    col2.metric(
        "🔥 Xu hướng",
        metrics["num_clusters"]
    )

    col3.metric(
        "🏢 Nguồn báo",
        article_df["source"].nunique()
    )

    col4.metric(
        "🏷️ Chủ đề",
        article_df["topic"].nunique()
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(
        "🎯 Tỷ lệ phân cụm",
        f"{metrics['cluster_coverage']:.2%}"
    )

    col2.metric(
        "⚪ Tỷ lệ nhiễu",
        f"{metrics['noise_ratio']:.2%}"
    )

    col3.metric(
        "📝 Từ/Tiêu đề",
        f"{article_df['title_word_count'].mean():.1f}"
    )

    col4.metric(
        "📄 Từ/Mô tả",
        f"{article_df['description_word_count'].mean():.1f}"
    )

    start = article_df["published"].min()
    end = article_df["published"].max()

    st.info(
        f"📅 Dữ liệu được thu thập từ **{start:%d/%m/%Y}** đến **{end:%d/%m/%Y}**."
    )