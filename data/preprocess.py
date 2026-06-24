import pandas as pd

def build_trend_dataframe(trends):
    rows = []

    for i, trend in enumerate(trends, start=1):
        rows.append(
            {
                "rank": int(trend.get("rank", i)),
                "cluster_id": trend.get("cluster_id", ""),
                "trend_name": trend.get("trend_name", trend.get("trend", "Xu hướng chưa đặt tên")),
                "shorten_trend_name": trend.get("trend_name", trend.get("trend", "Xu hướng chưa đặt tên"))[:100],
                "article_count": int(trend.get("article_count", trend.get("num_articles", 0)) or 0),
                "keywords": ", ".join(trend.get("keywords", []))
                if isinstance(trend.get("keywords", []), list)
                else trend.get("keywords", ""),
            }
        )

    return pd.DataFrame(rows)

def build_article_dataframe(trends):
    rows = []

    for trend in trends:
        for article in trend["articles"]:
            article = article.copy()
            article["cluster_id"] = trend["cluster_id"]
            article["trend_rank"] = trend["rank"]
            article["coherence"] = trend["coherence"]
            rows.append(article)

    article_df = pd.DataFrame(rows)
    article_df.head()

    article_df["title_word_count"] = (
        article_df["title"]
        .fillna("")
        .str.split()
        .str.len()
    )

    article_df["description_word_count"] = (
        article_df["description"]
        .fillna("")
        .str.split()
        .str.len()
    )

    article_df["title_char_count"] = (
        article_df["title"]
        .fillna("")
        .str.len()
    )

    article_df["description_char_count"] = (
        article_df["description"]
        .fillna("")
        .str.len()
    )

    article_df["published"] = pd.to_datetime(
        article_df["published"],
        utc=True
    )

    article_df["published_date"] = (
        article_df["published"].dt.date
    )

    article_df["published_hour"] = (
        article_df["published"].dt.hour
    )

    TOPIC_MAPPING = {
        "technology": "Công nghệ",
        "business": "Kinh doanh",
        "sports": "Thể thao",
        "sport": "Thể thao",
        "world": "Thế giới",
        "news": "Tin tức",
        "entertainment": "Giải trí",
        "education": "Giáo dục",
        "health": "Sức khỏe",
        "science": "Khoa học",
        "politics": "Chính trị",
        "lifestyle": "Đời sống",
        "travel": "Du lịch",
        "vehicles": "Xe cộ",
        "automotive": "Xe cộ",
        "law": "Pháp luật",
        "society": "Xã hội",
        "culture": "Văn hóa",
        "real_estate": "Bất động sản",
        "environment": "Môi trường",
        "travelling": "Du lịch"
    }

    article_df["topic_vi"] = article_df["topic"].map(
        lambda x: TOPIC_MAPPING.get(x, x)
    )

    return article_df
