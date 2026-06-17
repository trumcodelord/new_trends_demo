def get_article_title(article, fallback="Bài viết"):
    """Lấy tiêu đề từ nhiều schema khác nhau trong trends.json."""
    if not isinstance(article, dict):
        return str(article)
    return article.get("title") or article.get("headline") or fallback

def get_article_url(article):
    """Lấy URL từ nhiều schema khác nhau trong trends.json."""
    if not isinstance(article, dict):
        return ""
    return article.get("url") or article.get("link") or article.get("href") or ""

def get_article_source(article):
    """Lấy nguồn báo, nếu dữ liệu có sẵn."""
    if not isinstance(article, dict):
        return ""
    return article.get("source") or article.get("rss_source") or article.get("domain") or ""


def get_article_published(article):
    """Lấy ngày đăng, nếu dữ liệu có sẵn."""
    if not isinstance(article, dict):
        return ""
    return article.get("published") or article.get("date") or article.get("time") or ""