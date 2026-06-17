import streamlit as st

def render_header():
    st.markdown(
    """
    <div class="hero">
        <div class="pill">📰 Phân tích tin tức • Clustering • Tóm tắt bằng LLM</div>
        <h1 class="hero-title">Bảng điều khiển phát hiện xu hướng tin tức</h1>
        <div class="hero-subtitle">
            Trực quan hóa các cụm tin tức, số lượng bài viết và các xu hướng nổi bật được phát hiện tự động.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)