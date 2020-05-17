from rest_framework.pagination import LimitOffsetPagination


class PaginationWithDefaults(LimitOffsetPagination):
    default_limit = 10
    page_size_query_param = 'limit'
    offset_query_param = 'start'
    max_limit = 100