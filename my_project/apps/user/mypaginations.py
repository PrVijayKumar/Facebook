from rest_framework.pagination import PageNumberPagination, CursorPagination

class MyPageNumberPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'p'
    page_size_query_param = 'records'
    max_page_size = 8
    # last_page_strings = 'end'

class MyCursorPagination(CursorPagination):
    page_size = 5
    ordering = 'id'
    cursor_query_param = 'cur'
