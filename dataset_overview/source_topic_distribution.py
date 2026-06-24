import streamlit as st

def render_source_topic_distribution(article_df, metrics):
    source_stats = (
        article_df["source"]
        .value_counts()
        .reset_index()
    )

    source_stats.columns = [
        "Nguồn",
        "Số bài báo"
    ]

    topic_stats = (
        article_df["topic_vi"]
        .value_counts()
        .reset_index()
    )    
    
    topic_stats.columns = [
        "Chủ đề",
        "Số bài báo"
    ]

    st.subheader("📈 Chất lượng phân cụm")

    st.progress(metrics["cluster_coverage"])
    st.caption(
        f"<b>Tỷ lệ bài báo được phân cụm:</b> {metrics['cluster_coverage']:.2%}",
        unsafe_allow_html=True
    )

    left, right = st.columns(2)

    with left:
        st.subheader("📰 Phân bố nguồn báo")

        st.bar_chart(
            source_stats.set_index("Nguồn")
        )

    with right:
        st.subheader("🏷️ Phân bố chủ đề")

        st.bar_chart(
            topic_stats.set_index("Chủ đề")
        )