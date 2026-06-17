import streamlit as st
from datetime import datetime


def render_metrics(trends, metrics, model_info, generated_at):
    noise = metrics.get("noise_ratio")
    noise_text = f"{float(noise):.2%}" if isinstance(noise, (float, int)) else "N/A"

    c1, c2, c3, c4 = st.columns(4)

    cards = [
        ("Xu hướng phát hiện", len(trends), "📌"),
        ("Bài viết RSS", metrics.get("total_rss_articles", "N/A"), "🌐"),
        ("Bài viết thu thập", metrics.get("total_scraped_articles", "N/A"), "📰"),
        ("Tỷ lệ nhiễu", noise_text, "⚙️"),
    ]

    for col, (label, value, icon) in zip([c1, c2, c3, c4], cards):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{icon} {label}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    
    with st.expander("Thông tin mô hình và xử lý dữ liệu", expanded=False):
        m1, m2, m3, m4 = st.columns(4)

        m1.metric("Mô hình Embedding", model_info.get("embedding_model", "N/A"))
        m2.metric("Mô hình LLM", model_info.get("llm_model", "N/A"))
        m3.metric("Quantization", model_info.get("quantization", "N/A"))
        m4.metric("Độ liên kết cụm", f"{metrics['weighted_coherence']:.3f}" if "weighted_coherence" in metrics else "N/A")

        st.caption(f"Thời điểm tạo dữ liệu: {datetime.fromisoformat(generated_at).strftime('%Y-%m-%d %H:%M:%S') if generated_at else 'N/A'}")
