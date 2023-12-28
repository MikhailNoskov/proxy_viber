from rest_framework import viewsets, status
from rest_framework.response import Response


class ViberMessage(viewsets.ViewSet):
    def create(self, request):
        data = request.data
        print(data)
        return Response(status=status.HTTP_200_OK)
