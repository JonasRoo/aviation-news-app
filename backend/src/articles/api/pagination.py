from rest_framework.pagination import PageNumberPagination


class ArticlePagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "pageSize"
    max_page_size = 500
