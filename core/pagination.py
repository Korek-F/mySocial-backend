from rest_framework.pagination import PageNumberPagination 
from rest_framework.response import Response

class MyPagination(PageNumberPagination):
    page = 1
    page_size = 5
    page_size_query_param= 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'data':data,
            'meta':{
                'all_data':self.page.paginator.count,
                'page':int(self.request.GET.get('page',1)),
                'page_size': int(self.request.GET.get('page_size', 5)),
                'next':self.get_next_link(),
                'previous': self.get_previous_link()
                }
        })