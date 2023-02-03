from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
        # # max_page_size = 5
    def get_paginated_response(self, data):
        return Response({
            'total_objects': self.page.paginator.count,
            'page_size': self.page_size,
            'total_pages': self.page.paginator.num_pages,
            'current_page_number': self.page.number,
            'next': self.page.number + 1 ,
            'previous': self.page.number - 1,
            'results': data
        })

