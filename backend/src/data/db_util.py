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

    try:
        articles.to_csv(file_path, index=False, encoding="utf-8-sig")
    except PermissionError:
        desired_file_name = os.path.basename(file_path)
        file_name_components = list(os.path.splitext(desired_file_name))
        file_name_components[0] = file_name_components[0] + "_new"
        new_assigned_file_name = "".join(file_name_components)
        articles.to_csv(new_assigned_file_name, index=False, encoding="utf-8-sig")

