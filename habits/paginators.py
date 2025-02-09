from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """
    Пользовательская пагинация для API.

    Атрибуты:
        page_size (int): Количество объектов на странице (по умолчанию 5).
        page_size_query_param (str): Параметр запроса, который позволяет клиенту
                                      указывать желаемое количество объектов на странице.
        max_page_size (int): Максимально допустимое количество объектов на странице (по умолчанию 10).
    """

    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 10
