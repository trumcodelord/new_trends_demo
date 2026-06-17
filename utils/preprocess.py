import pandas as pd

def build_trend_dataframe(trends):
    rows = []

    for i, trend in enumerate(trends, start=1):
        rows.append(
            {
                "rank": int(trend.get("rank", i)),
                "cluster_id": trend.get("cluster_id", ""),
                "trend_name": trend.get("trend_name", trend.get("trend", "Xu hướng chưa đặt tên"))[:100],
                "article_count": int(trend.get("article_count", trend.get("num_articles", 0)) or 0),
                "keywords": ", ".join(trend.get("keywords", []))
                if isinstance(trend.get("keywords", []), list)
                else trend.get("keywords", ""),
            }
        )

    return pd.DataFrame(rows)
