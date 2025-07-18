from rest_framework.pagination import LimitOffsetPagination

class MyPagination(LimitOffsetPagination):
    default_limit = 100
    max_limit = 100
    limit_query_param = 'limit'
    offset_query_param = 'offset'