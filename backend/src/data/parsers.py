from typing import List, Dict, Tuple

from datetime import datetime
from dateutil import parser as dateutil_parser
from bs4 import BeautifulSoup

from .base_parser import BaseEndpointParser


class AviationWeekMROParser(BaseEndpointParser):
    def __init__(self, end_date: datetime):
        self.end_date = end_date
        super().__init__(source_name="https://aviationweek.com")
        self.article_element_selector = ("div", {"class": "articles-list__block"})

        self.url = "https://aviationweek.com/views/ajax?_wrapper_format=drupal_ajax"
        self.method = "POST"
        self.page_arg = ("page", 37)
        self.payload = {
            "view_name": "article_list_automated_",
            "view_display_id": "block_standard",
            "view_args": "316",
            "view_path": "/node/1467591",
            "view_base_path": "",
            "view_dom_id": "f33f0e285e4f4ce93842d0491d6919824fa87d7ab8e37447ced508e15300dd21",
            "pager_element": "0",
            "page": "1",
            "content_source[0][target_id]": "35721",
            "_drupal_ajax": "1",
            "ajax_page_state[theme]": "particle",
            "ajax_page_state[theme_token]": "",
            "ajax_page_state[libraries]": "awn_adobe_launch/adobe_launch,awn_adobe_launch/media_tracking,awn_adobe_launch/visitor_params,awn_core/gdpr-compliance,awn_dfp/dfp_gallery,awn_dfp/dfp_referring_category,awn_eloqua/awn-eloqua,awn_group/awn_group,awn_user/awn.user,core/drupal.autocomplete,core/html5shiv,lazy/lazy,paragraphs/drupal.paragraphs.unpublished,particle/core,simple_popup_blocks/simple_popup_blocks,system/base,views/views.ajax,views/views.module,views_infinite_scroll/views-infinite-scroll",
        }
        self.wait_time = (2.5, 3.0)

    def pipe(self, data: Dict[str, str]) -> Tuple[List[Dict[str, str]], bool]:
        raw_html = self.extract_data_field(data=data)
        soup = BeautifulSoup(raw_html)
        articles = self.extract_and_parse_html_to_articles(soup=soup)
        parsed_articles, should_stop = [], False
        for article in articles:
            try:
                parsed_article = self.parse_article(article=article)
            except:
                print(f"Error parsing article {article}. Skipping..")
                continue
            if parsed_article.get("date_published", datetime.today()) < self.end_date:
                should_stop = True
                break
            parsed_articles.append(parsed_article)

        return parsed_articles, should_stop

    def extract_data_field(self, data: Dict[str, str]) -> BeautifulSoup:
        return data[1]["data"]

    def extract_and_parse_html_to_articles(
        self, soup: BeautifulSoup
    ) -> List[BeautifulSoup]:
        return soup.find("div").find_all(*self.article_element_selector)

    def parse_article(self, article: List[BeautifulSoup]) -> Dict[str, str]:
        r = {}
        r["source"] = self.source_name
        try:
            r["image"] = "".join(
                [
                    r["source"],
                    article.find("div", {"class": "articles-list__image"}).find("img")[
                        "src"
                    ],
                ]
            )
        except:
            r["image"] = ""
        article = article.find("div", {"class": "articles-list__content"})

        r["title"] = (
            article.find("div", {"class": "articles-list__title"})
            .find("a")
            .find("span")
            .contents[0]
        )
        r["link"] = "".join(
            [
                r["source"],
                article.find("div", {"class": "articles-list__title"}).find("a")[
                    "href"
                ],
            ]
        )
        r["date_published"] = dateutil_parser.parse(
            article.find("div", {"class": "articles-list__date"}).contents[0]
        )
        try:
            r["description"] = article.find(
                "div", {"class": "articles-list__description"}
            ).contents[0]
        except:
            r["description"] = ""
        r["author"] = ""

        return super().unicode_normalize_dict(data=r)
