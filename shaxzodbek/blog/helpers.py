def group_articles(data) -> dict:
    grouped_articles = {}
    for article in data:
        year = article.created.year
        month = article.created.month

        if year not in grouped_articles:
            grouped_articles[year] = {}

        if month not in grouped_articles[year]:
            grouped_articles[year][month] = []

        grouped_articles[year][month].append(article)
    return grouped_articles


def make_unique(data):
    return set(i.name for i in data)
