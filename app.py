from pathlib import Path

import streamlit as st
from streamlit_theme import st_theme

from data.loader import load_payload
from data.preprocess import build_trend_dataframe, build_article_dataframe

from general.sidebar import render_sidebar, filter_trends
from general.header import render_header
from general.metrics import render_metrics

from dataset_overview.dataset_overview import render_dataset_overview

from eda_analysis.eda_analysis import render_eda_analysis

from embedding_anslysis.embedding_umap import plot_umap

from trends_analysis.trend_size_coherence_scatter_plot import plot_trend_size_scatter
from trends_analysis.source_trend_heatmap import plot_source_trend_heatmap
from trends_analysis.trend_size_bar_chart import plot_trend_size_bar_chart

from trends_analysis.trend_table import render_trend_table
from trend_detail_analysis.trend_detail import render_trend_detail


DATA_PATH = Path("trends.json")
TABLE_HEIGHT = 420
UMAP_HEIGHT = 700
HEATMAP_HEIGHT = 700
SCATTER_HEIGHT = 700


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
    with open("assets/style_light_mode.css", encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True,
        )
else:
    with open("assets/style_dark_mode.css", encoding="utf-8") as f:
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
article_df = build_article_dataframe(trends)

# =========================================================
# Sidebar
# =========================================================
filters = render_sidebar(trend_df)

filtered_df = filter_trends(
    trend_df,
    filters,
    article_df,
)

# =========================================================
# Header
# =========================================================
render_header()

render_metrics(trends, metrics, model_info, generated_at)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Tổng quan dữ liệu",
    "Phân tích EDA",
    "Phân tích embedding",
    "Phân tích cụm",
    "Phân tích chi tiết cụm",
])

with tab1:
    render_dataset_overview(article_df, metrics)

with tab2:
    render_eda_analysis(article_df)

with tab3:
    # =========================================================
    # UMAP plot
    # =========================================================
    plot_umap(trends, UMAP_HEIGHT)

with tab4:
    # =========================================================
    # Heatmap plot
    # =========================================================
    plot_source_trend_heatmap(trends, trend_df, filters, HEATMAP_HEIGHT)

    # =========================================================
    # Scatter plot
    # =========================================================
    plot_trend_size_scatter(trends, SCATTER_HEIGHT)

    # =========================================================
    # Chart
    # =========================================================
    plot_trend_size_bar_chart(filtered_df, filters)

    # =========================================================
    # Danh sách xu hướng
    # =========================================================
    render_trend_table(filtered_df, TABLE_HEIGHT)

with tab5:
    # =========================================================
    # Chi tiết xu hướng
    # =========================================================
    render_trend_detail(
        trends,
        filtered_df,
        TABLE_HEIGHT,
    )


st.markdown("---")
st.caption("IT4930 - News Trend Detection | Semester 2025.2")
