from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class MyPageNumberPagination(PageNumberPagination):
    page_size = settings.REST_FRAMEWORK["PAGE_SIZE"] or 10
    page_query_param = "page"
    max_page_size = 100
    page_size_query_param = "items"
