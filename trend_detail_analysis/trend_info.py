import streamlit as st

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