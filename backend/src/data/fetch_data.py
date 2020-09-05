from .adapter import EndpointAdapter
from .parsers import AviationWeekMROParser

from articles.models import Article

from datetime import datetime


def fetch_data_for_aviationweek_mro():
    parser = AviationWeekMROParser(end_date=datetime(2018, 1, 1))

    adapter = EndpointAdapter(
        url=parser.url,
        method=parser.method,
        page_arg=parser.page_arg,
        payload=parser.payload,
        wait_time=parser.wait_time,
        parser=parser,
    )

    unique_fields = ("source", "title")

    for parsed_articles in adapter:
        for parsed_article in parsed_articles:
            article, created = Article.objects.update_or_create(
                **{k: v for k, v in parsed_article.items() if k in unique_fields},
                defaults={
                    k: v for k, v in parsed_article.items() if k not in unique_fields
                },
            )
            article.save()

            print(f"Writing article to DB:\n{article}")
            if not created:
                print(f">>>> This article was NOT created, only updated!!!")
