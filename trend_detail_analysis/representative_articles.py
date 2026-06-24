import streamlit as st


def render_representative_articles(representative_articles):
    if not representative_articles:
        return

    st.markdown(
        '<div class="section-title">Bài viết đại diện',
        unsafe_allow_html=True
    )

    rep_cols = st.columns(min(3, len(representative_articles)))

    for i, article in enumerate(representative_articles[:6], start=1):
        title = article.get("title", f"Bài viết {i}")
        url = article.get("title", "")
        published = article.get("published", "")

        with rep_cols[(i - 1) % len(rep_cols)]:
            with st.container(border=True):
                st.markdown("📰")
                st.markdown(f"**{title}**")
                if published:
                    st.caption(published)
                else:
                    st.caption("Bài đại diện")

                if url:
                    st.link_button("🔗 Mở bài gốc", url, use_container_width=True)
                else:
                    st.caption("Không có link bài gốc")