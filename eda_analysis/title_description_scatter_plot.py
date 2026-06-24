import streamlit as st
import plotly.express as px

def render_title_description_word_count_scatter_plot(filtered_df):
    st.markdown(
        '<div class="section-title">Biểu đồ phân tán độ dài tiêu đề và mô tả</div>',
        unsafe_allow_html=True,
    )

    fig = px.scatter(
        filtered_df,
        x="title_word_count",
        y="description_word_count",
        color="topic_vi",
        hover_name="title",
        custom_data=[
            "source",
            "published",
            "topic_vi"
        ],
        labels={
            "title_word_count": "Số từ tiêu đề",
            "description_word_count": "Số từ mô tả",
        },
        render_mode="svg",
    )

    fig.update_traces(
        hovertemplate=(
            "<b>%{hovertext}</b><br><br>"
            "<b>Chủ đề:</b> %{customdata[2]}<br>"
            "<b>Nguồn:</b> %{customdata[0]}<br>"
            "<b>Ngày:</b> %{customdata[1]|%d/%m/%Y}<br>"
            "<b>Tiêu đề:</b> %{x} từ<br>"
            "<b>Mô tả:</b> %{y} từ"
            "<extra></extra>"
        ),
        marker=dict(
            size=6,
            opacity=0.65,
            line=dict(width=0.3, color="white"),
        )
    )

    mean_title = filtered_df["title_word_count"].mean()
    mean_desc = filtered_df["description_word_count"].mean()

    fig.add_vline(
        x=mean_title,
        line_dash="dash",
        line_color="gray",
        annotation_text=f"Trung bình tiêu đề: {mean_title:.1f}",
        annotation_position="top"
    )

    fig.add_hline(
        y=mean_desc,
        line_dash="dash",
        line_color="gray",
        annotation_text=f"Trung bình mô tả: {mean_desc:.1f}",
        annotation_position="top left",
    )

    corr = filtered_df["title_word_count"].corr(
        filtered_df["description_word_count"]
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Tương quan",
        f"{corr:.2f}"
    )

    col2.metric(
        "Trung bình độ dài tiêu đề",
        f"{mean_title:.1f}"
    )

    col3.metric(
        "Trung bình độ dài mô tả",
        f"{mean_desc:.1f}"
    )

    fig.update_layout(
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(180,180,180,0.2)"
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(180,180,180,0.2)"
        ),
    )

    fig.update_layout(
        legend_title="Chủ đề",
        legend=dict(
            orientation="h",
            y=1.05,
            x=0
        )
    )

    fig.update_xaxes(
        range=[
            0,
            filtered_df["title_word_count"].max() + 2
        ]
    )

    fig.update_yaxes(
        range=[
            0,
            filtered_df["description_word_count"].max() + 5
        ]
    )

    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})