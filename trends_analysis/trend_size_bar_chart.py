import pandas as pd
import plotly.express as px
import streamlit as st


def plot_trend_size_bar_chart(filtered_df, filters):
    st.markdown(
        '<div class="section-title">Top xu hướng theo số lượng bài viết</div>',
        unsafe_allow_html=True,
    )

    chart_df = filtered_df.sort_values("article_count", ascending=False).head(filters["top_n"])

    if chart_df.empty:
        st.warning("Không có xu hướng nào khớp với bộ lọc hiện tại.")
        st.stop()

    if len(chart_df) == 1:
        row = chart_df.iloc[0]

        st.markdown(
            f"""
            <div class="single-result-card">
                <div class="single-result-label">Kết quả nổi bật khi lọc dữ liệu</div>
                <div class="single-result-title">{row['trend_name']}</div>
                <div class="single-result-meta">
                    <span class="mini-chip">📌 Xếp hạng #{row['rank']}</span>
                    <span class="mini-chip">🧩 Cụm {row['cluster_id']}</span>
                    <span class="mini-chip">📰 {row['article_count']} bài viết</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:
        fig = px.bar(
            chart_df.sort_values("article_count", ascending=True),
            x="article_count",
            y="shorten_trend_name",
            orientation="h",
            text="article_count",
            color="article_count",
            color_continuous_scale="Blues",
            custom_data=["trend_name"]
        )

        fig.update_traces(
            textposition="outside",
            marker_line_width=0,
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "<b>Số bài viết:</b> %{x}<extra></extra>"
            ),
            cliponaxis=False,
        )

        fig.update_layout(
            height=max(360, 38 * len(chart_df) + 90),
            margin=dict(l=12, r=52, t=12, b=28),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15,23,42,0.22)",
            font=dict(color="#E5E7EB", size=13),
            xaxis=dict(
                title="Số lượng bài viết",
                gridcolor="rgba(148,163,184,.13)",
                zeroline=False,
            ),
            yaxis=dict(
                title="",
                gridcolor="rgba(148,163,184,.04)",
                automargin=True,
                tickfont=dict(size=12),
            ),
            coloraxis_showscale=False,
            bargap=0.30,
        )

        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})