from rest_framework import pagination


class TenPageNumberPagination(pagination.PageNumberPagination):
    page_size = 1000
    page_query_param = 'page'
    page_size_query_param = 'size'
    max_page_size = 2000
