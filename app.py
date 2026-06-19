from pathlib import Path

import streamlit as st
from streamlit_theme import st_theme

from data.loader import load_payload
from utils.preprocess import build_trend_dataframe

from components.sidebar import render_sidebar, filter_trends
from components.header import render_header
from components.metrics import render_metrics

from charts.umap import plot_umap
from charts.heatmap import plot_heatmap
from charts.trend_bar import plot_trend_bar

from components.trend_table import render_trend_table
from components.trend_detail import render_trend_detail



DATA_PATH = Path("trends.json")
MAX_TREND_NAME_LENGTH = 100
TABLE_HEIGHT = 420
UMAP_HEIGHT = 700
HEATMAP_HEIGHT = 700



st.set_page_config(
    page_title="Phát hiện xu hướng tin tức",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded",
)

if not DATA_PATH.exists():
    st.error("Không tìm thấy file trends.json. Hãy đặt trends.json cùng thư mục với app.py.")
    st.stop()


# =========================================================
# CSS
# =========================================================
theme = st_theme()

if theme and theme["base"] == "light":
    with open("assets/style_light_mode.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True,
        )
else:
    with open("assets/style_dark_mode.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True,
        )


trends, metrics, model_info, generated_at = load_payload(str(DATA_PATH))

if not trends:
    st.warning("File trends.json có tồn tại nhưng không có xu hướng nào.")
    st.stop()


# =========================================================
# Chuẩn hóa dữ liệu
# =========================================================
trend_df = build_trend_dataframe(trends)

# =========================================================
# Sidebar
# =========================================================
filters = render_sidebar(trend_df)

filtered_df = filter_trends(
    trend_df,
    filters
)

# =========================================================
# Header
# =========================================================
render_header()

render_metrics(trends, metrics, model_info, generated_at)

# =========================================================
# UMAP plot
# =========================================================

st.markdown(
    '<div class="section-title">Biểu đồ UMAP các cụm xu hướng</div>',
    unsafe_allow_html=True,
)

plot_umap(trends, UMAP_HEIGHT)

# =========================================================
# Heatmap plot
# =========================================================

st.markdown(
    '<div class="section-title">Biểu đồ Heatmap các cụm xu hướng</div>',
    unsafe_allow_html=True,
)

plot_heatmap(trends, trend_df, filters, MAX_TREND_NAME_LENGTH, HEATMAP_HEIGHT)

# =========================================================
# Chart
# =========================================================
plot_trend_bar(filtered_df, filters)

# =========================================================
# Danh sách xu hướng
# =========================================================
render_trend_table(filtered_df, TABLE_HEIGHT)

# =========================================================
# Chi tiết xu hướng
# =========================================================
render_trend_detail(
    trends,
    filtered_df,
    TABLE_HEIGHT
)


st.markdown("---")
st.caption("IT4930 - News Trend Detection | Semester 2025.2")