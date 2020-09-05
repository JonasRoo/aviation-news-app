from bs4 import BeautifulSoup
import unicodedata

from typing import Dict, List


class BaseEndpointParser:
    def __init__(self, source_name: str, *args, **kwargs):
        self.source_name = source_name

    def pipe(self, data: Dict[str, str]):
        # raise NotImplementedError(f"Subclass needs to overwrite this method!")
        raw_html = self.extract_data_field(data=data)
        soup = BeautifulSoup(raw_html)
        articles = self.extract_and_parse_html_to_articles(soup=soup)
        parsed_articles = []
        for article in articles:
            parsed_articles.append(self.parse_article(article=article))

    def extract_data_field(self, data: Dict[str, str]) -> BeautifulSoup:
        raise NotImplementedError(f"Subclass needs to overwrite this method!")

    def extract_and_parse_html_to_articles(
        self, soup: BeautifulSoup
    ) -> List[BeautifulSoup]:
        raise NotImplementedError(f"Subclass needs to overwrite this method!")

    def parse_article(self, article: BeautifulSoup) -> Dict[str, str]:
        raise NotImplementedError(f"Subclass needs to overwrite this method!")

    @staticmethod
    def unicode_normalize_dict(data: Dict[str, str]) -> Dict[str, str]:
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = unicodedata.normalize("NFKD", value)

        return data
