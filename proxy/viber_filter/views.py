from rest_framework import viewsets, status
from rest_framework.response import Response

from viber_filter.services import add_to_queue


class ViberMessage(viewsets.ViewSet):
    @staticmethod
    def create(request):
        response = add_to_queue(request.data)
        return Response(data=response, status=status.HTTP_200_OK)
