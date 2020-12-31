from articles.models import Article

import pandas as pd
import os


def write_all_articles_to_csv(file_path: str = "./data.csv", query=None):
    if query is not None:
        queryset = Article.objects.filter(query)
    else:
        queryset = Article.objects.all()
    if not queryset:
        raise ValueError("There are no articles matching this query!")
    list_of_columns = [
        "source",
        "title",
        "link",
        "date_published",
        "description",
        "image",
        "author",
    ]

    articles = pd.DataFrame.from_records(queryset.values_list(*list_of_columns))
    articles.columns = list_of_columns
    articles.date_published = pd.to_datetime(articles.date_published).dt.date
    articles.description, articles.title = (
        articles.description.str.replace("\n", " "),
        articles.title.str.replace("\n", " "),
    )

    if os.path.isfile(file_path):
        from time import time

        directory, file_name = os.path.split(file_path)
        new_file_name = str(int(time())) + file_name
        file_path = os.path.join(directory, new_file_name)

    articles.to_csv(file_path, sep=";", index=False, encoding="utf-8-sig")
