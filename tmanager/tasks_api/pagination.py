from rest_framework.pagination import PageNumberPagination


class ApiViewPaginator(PageNumberPagination):
    page_size = 10
