import logging

from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status

from .exceptions import *
from .models import *
from .serializers import *

logger = logging.getLogger('API VIEWS')


class RetrieveUpdateDestroyBoardApiView(RetrieveUpdateDestroyAPIView):

    lookup_field = 'pk'
    serializer_class = BoardSerializer

    def get_object(self):
        return Board.objects.get(pk=self.kwargs.get(self.lookup_field))

    def get(self, request, *args, **kwargs):
        """
        Get board by its unique identifier.
            :param request: DRF request.
            :returns Response: REST API response.
            :raises NotFound: if board with pk has not been found.
        """
        try:
            board_object = self.get_object()
        except Board.DoesNotExist:
            logging.info(msg='Requested board has not been found on server.')
            raise NotFound('Object does not exist.')

        serialized_object = self.serializer_class(board_object)
        return Response(serialized_object.data)

    def update(self, request, *args, **kwargs):
        """
        Updates board by Its unique identifier.
            :param request:
            :returns Response: REST API response.
            :raises ValidationError: if board has validation errors.
        """


class CreateBoardApiView(CreateAPIView):

    serializer_class = BoardSerializer

    def post(self, request, **kwargs):
        """
        Creates new board.
            :param request: DRF request.
            :returns Response: REST API response.
            :raises ValidationError: if board has validation errors.
        """

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logging.error('Can not create Boarder object. Invalid data.')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


__all__ = [
    'RetrieveUpdateDestroyBoardApiView',
    'CreateBoardApiView',
]
