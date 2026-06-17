import streamlit as st

def render_trend_table(filtered_df, table_height):

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

        st.dataframe(display_df, width="stretch", hide_index=True, height=table_height)

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