from rest_framework.pagination import PageNumberPagination


class QuestionsPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = "page"
