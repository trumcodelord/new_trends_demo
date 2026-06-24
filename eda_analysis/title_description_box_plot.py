import pandas as pd
import plotly.express as px
import streamlit as st

def render_title_boxplot(filtered_df):
    st.markdown(
        '<div class="section-title">Biểu đồ hộp độ dài tiêu đề theo chủ đề</div>',
        unsafe_allow_html=True,
    )

    topic_order = (
        filtered_df["topic_vi"]
        .value_counts()
        .index
        .tolist()
    )

    fig = px.box(
        filtered_df,
        x="topic_vi",
        y="title_word_count",
        color="topic_vi",
        category_orders={
            "topic_vi": topic_order
        }
    )

    fig.update_layout(
        xaxis_title="Chủ đề",
        yaxis_title="Số từ"
    )

    fig.update_traces(
        boxpoints="outliers"
    )

    fig.update_traces(
        hovertemplate=(
            "<b>Chủ đề:</b> %{x}<br>"
            "<b>Số từ:</b> %{y}"
            "<extra></extra>"
        )
    )

    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

def render_description_boxplot(filtered_df):
    st.markdown(
        '<div class="section-title">Biểu đồ hộp độ dài mô tả theo chủ đề</div>',
        unsafe_allow_html=True,
    )

    topic_order = (
        filtered_df["topic_vi"]
        .value_counts()
        .index
        .tolist()
    )

    fig = px.box(
        filtered_df,
        x="topic_vi",
        y="description_word_count",
        color="topic_vi",
        category_orders={
            "topic_vi": topic_order
        }
    )

    fig.update_layout(
        xaxis_title="Chủ đề",
        yaxis_title="Số từ"
    )

    fig.update_traces(
        boxpoints="outliers"
    )

    fig.update_traces(
        hovertemplate=(
            "<b>Chủ đề:</b> %{x}<br>"
            "<b>Số từ:</b> %{y}"
            "<extra></extra>"
        )
    )

    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})