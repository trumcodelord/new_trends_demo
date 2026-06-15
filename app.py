import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Bảng điều khiển phát hiện xu hướng tin tức",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CSS
# =========================================================
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0B1020 0%, #111827 45%, #0F172A 100%);
        color: #F8FAFC;
    }

    section[data-testid="stSidebar"] {
        background: #0F172A;
        border-right: 1px solid rgba(148, 163, 184, 0.18);
    }

    .block-container {
        padding-top: 2.1rem;
        padding-bottom: 3rem;
        max-width: 1320px;
    }

    .hero {
        padding: 28px 32px;
        border-radius: 24px;
        background:
            radial-gradient(circle at top left, rgba(56,189,248,.22), transparent 32%),
            linear-gradient(135deg, rgba(30,41,59,.95), rgba(15,23,42,.95));
        border: 1px solid rgba(148, 163, 184, 0.24);
        box-shadow: 0 20px 60px rgba(0,0,0,.25);
        margin-bottom: 22px;
    }

    .hero-title {
        font-size: 44px;
        font-weight: 900;
        line-height: 1.05;
        letter-spacing: -0.04em;
        margin: 0;
        color: #F8FAFC;
    }

    .hero-subtitle {
        margin-top: 12px;
        color: #CBD5E1;
        font-size: 16px;
    }

    .pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 7px 12px;
        border-radius: 999px;
        background: rgba(14, 165, 233, .14);
        border: 1px solid rgba(56,189,248,.32);
        color: #BAE6FD;
        font-size: 13px;
        font-weight: 700;
        margin-bottom: 14px;
    }

    .metric-card {
        padding: 20px 22px;
        border-radius: 20px;
        background: rgba(15,23,42,.72);
        border: 1px solid rgba(148, 163, 184, 0.20);
        box-shadow: 0 14px 32px rgba(0,0,0,.20);
        min-height: 120px;
    }

    .metric-label {
        color: #94A3B8;
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: .06em;
    }

    .metric-value {
        color: #F8FAFC;
        font-size: 36px;
        font-weight: 900;
        letter-spacing: -0.03em;
        margin-top: 10px;
    }

    .section-title {
        margin-top: 30px;
        margin-bottom: 14px;
        font-size: 26px;
        font-weight: 900;
        color: #F8FAFC;
        letter-spacing: -0.03em;
    }

    .trend-card {
        padding: 22px 24px;
        border-radius: 22px;
        background: rgba(15,23,42,.78);
        border: 1px solid rgba(148, 163, 184, 0.20);
        box-shadow: 0 14px 36px rgba(0,0,0,.22);
        margin-bottom: 16px;
    }

    .trend-rank {
        color: #38BDF8;
        font-size: 13px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: .08em;
    }

    .trend-title {
        color: #F8FAFC;
        font-size: 22px;
        font-weight: 850;
        margin-top: 6px;
        margin-bottom: 12px;
        line-height: 1.25;
    }

    .trend-meta {
        color: #94A3B8;
        font-size: 14px;
    }

    div[data-testid="stMetric"] {
        background: rgba(15,23,42,.72);
        border: 1px solid rgba(148, 163, 184, 0.20);
        border-radius: 18px;
        padding: 18px;
    }

    div[data-testid="stMetricValue"] {
        color: #F8FAFC;
        font-weight: 900;
    }

    div[data-testid="stMetricLabel"] {
        color: #CBD5E1;
        font-weight: 700;
    }

    .stDataFrame {
        border-radius: 18px;
        overflow: hidden;
    }

    hr {
        border-color: rgba(148, 163, 184, 0.2);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


DATA_PATH = Path("trends.json")


@st.cache_data(show_spinner=False)
def load_payload(path: str):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        return (
            data.get("trends", []),
            data.get("metrics", {}),
            data.get("model", {}),
            data.get("generated_at", ""),
        )

    return data, {}, {}, ""


if not DATA_PATH.exists():
    st.error("Không tìm thấy file trends.json. Hãy đặt trends.json cùng thư mục với app.py.")
    st.stop()

trends, metrics, model_info, generated_at = load_payload(str(DATA_PATH))

if not trends:
    st.warning("File trends.json có tồn tại nhưng không có xu hướng nào.")
    st.stop()


# =========================================================
# Chuẩn hóa dữ liệu
# =========================================================
rows = []

for i, trend in enumerate(trends, start=1):
    rows.append(
        {
            "rank": int(trend.get("rank", i)),
            "cluster_id": trend.get("cluster_id", ""),
            "trend_name": trend.get("trend_name", trend.get("trend", "Xu hướng chưa đặt tên")),
            "article_count": int(trend.get("article_count", trend.get("num_articles", 0)) or 0),
            "keywords": ", ".join(trend.get("keywords", []))
            if isinstance(trend.get("keywords", []), list)
            else trend.get("keywords", ""),
        }
    )

trend_df = pd.DataFrame(rows)


# =========================================================
# Sidebar
# =========================================================
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


filtered_df = trend_df[trend_df["article_count"] >= min_articles].copy()

if search_text:
    q = search_text.lower()
    filtered_df = filtered_df[
        filtered_df["trend_name"].str.lower().str.contains(q, na=False)
        | filtered_df["keywords"].str.lower().str.contains(q, na=False)
    ]


# =========================================================
# Header
# =========================================================
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
    m4.metric("Độ liên kết cụm", metrics.get("weighted_coherence", "N/A"))

    st.caption(f"Thời điểm tạo dữ liệu: {generated_at if generated_at else 'N/A'}")


# =========================================================
# Chart
# =========================================================
st.markdown(
    '<div class="section-title">Top xu hướng theo số lượng bài viết</div>',
    unsafe_allow_html=True,
)

chart_df = filtered_df.sort_values("article_count", ascending=False).head(top_n)

if chart_df.empty:
    st.warning("Không có xu hướng nào khớp với bộ lọc hiện tại.")
    st.stop()

fig = px.bar(
    chart_df.sort_values("article_count", ascending=True),
    x="article_count",
    y="trend_name",
    orientation="h",
    text="article_count",
    color="article_count",
    color_continuous_scale="Blues",
)

fig.update_traces(
    textposition="outside",
    marker_line_width=0,
    hovertemplate="<b>%{y}</b><br>Số bài viết: %{x}<extra></extra>",
)

fig.update_layout(
    height=max(440, 34 * len(chart_df) + 140),
    margin=dict(l=20, r=40, t=20, b=20),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(15,23,42,0.35)",
    font=dict(color="#E5E7EB", size=13),
    xaxis=dict(
        title="Số lượng bài viết",
        gridcolor="rgba(148,163,184,.16)",
        zeroline=False,
    ),
    yaxis=dict(
        title="",
        gridcolor="rgba(148,163,184,.05)",
    ),
    coloraxis_showscale=False,
)

st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# =========================================================
# Danh sách xu hướng
# =========================================================
st.markdown(
    '<div class="section-title">Danh sách xu hướng phát hiện</div>',
    unsafe_allow_html=True,
)

left, right = st.columns([1.15, 1])

with left:
    display_df = filtered_df.sort_values("article_count", ascending=False)[
        ["rank", "trend_name", "article_count", "cluster_id"]
    ].rename(
        columns={
            "rank": "Xếp hạng",
            "trend_name": "Tên xu hướng",
            "article_count": "Số bài viết",
            "cluster_id": "Mã cụm",
        }
    )

    st.dataframe(display_df, use_container_width=True, hide_index=True, height=420)

with right:
    best = filtered_df.sort_values("article_count", ascending=False).head(3)

    for _, row in best.iterrows():
        st.markdown(
            f"""
            <div class="trend-card">
                <div class="trend-rank">Top #{row['rank']} • Cụm {row['cluster_id']}</div>
                <div class="trend-title">{row['trend_name']}</div>
                <div class="trend-meta">📰 {row['article_count']} bài viết liên quan</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# =========================================================
# Chi tiết xu hướng
# =========================================================
st.markdown(
    '<div class="section-title">Chi tiết xu hướng</div>',
    unsafe_allow_html=True,
)

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

if selected_trend is None:
    st.error("Không tìm thấy xu hướng đã chọn.")
    st.stop()

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


representative_articles = selected_trend.get("representative_articles", [])

if representative_articles:
    st.markdown("#### Bài viết đại diện")

    for i, article in enumerate(representative_articles, start=1):
        title = article.get("title", f"Bài viết {i}") if isinstance(article, dict) else str(article)
        url = article.get("url", "") if isinstance(article, dict) else ""

        if url:
            st.markdown(f"{i}. [{title}]({url})")
        else:
            st.markdown(f"{i}. {title}")


all_articles = selected_trend.get("articles", selected_trend.get("all_articles", []))
article_rows = []

for i, article in enumerate(all_articles, start=1):
    if isinstance(article, dict):
        article_rows.append(
            {
                "STT": i,
                "Tiêu đề": article.get("title", ""),
                "Nguồn": article.get("source", ""),
                "Ngày đăng": article.get("published", article.get("date", "")),
                "Liên kết": article.get("url", article.get("link", "")),
            }
        )
    else:
        article_rows.append(
            {
                "STT": i,
                "Tiêu đề": str(article),
                "Nguồn": "",
                "Ngày đăng": "",
                "Liên kết": "",
            }
        )

if article_rows:
    st.markdown("#### Tất cả bài viết trong cụm")

    st.dataframe(
        pd.DataFrame(article_rows),
        use_container_width=True,
        hide_index=True,
        height=360,
    )


st.markdown("---")
st.caption("IT4930 - News Trend Detection | Semester 2025.2")
