from rest_framework import viewsets, status
from rest_framework.response import Response

from viber_filter.services import add_to_queue, log_main


class ViberMessage(viewsets.ViewSet):
    http_method_names = ('post',)

    @staticmethod
    def create(request):
        # print(request.headers)
        response = add_to_queue(request.data)
        return Response(data=response, status=status.HTTP_200_OK)


class MainService(viewsets.ViewSet):
    http_method_names = ('post',)

    @staticmethod
    def create(request):
        log_main(request.headers['X-Celery-ID'], request.data)
        return Response(status=status.HTTP_201_CREATED)
