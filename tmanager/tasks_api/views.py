import logging

from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import *
from .serializers import *

logger = logging.getLogger('API VIEWS')


class BaseRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    lookup_field = 'pk'
    serializer_class = None
    model = None
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return self.model.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs.get(self.lookup_field))
        return obj

    def get(self, request, *args, **kwargs):
        """
        Get object by its unique identifier.
            :param request: HTTP GET request.
            :returns Response: REST API response.
            :raises NotFound: if object with pk has not been found.
        """
        obj = self.get_object()
        serializer = self.serializer_class(obj)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        """
        Updates object by Its unique identifier.
            :param request: HTTP PUT request.
            :returns Response: REST API response.
            :raises ValidationError: if object has validation errors.
        """
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """
        Removes object by Its unique identifier.
            :param request: HTTP DELETE request.
            :returns Response: REST API response.
        """
        instance = self.get_object()
        user = request.user

        if not instance.can_be_destroyed(user):
            return Response({"error": "Only staff can delete boards."}, status=status.HTTP_403_FORBIDDEN)

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BaseCreateApiView(CreateAPIView):

    model = None
    serializer_class = None
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    def post(self, request, **kwargs):
        """
        Creates new object.
            :param request: HTTP POST request.
            :returns Response: REST API response.
            :raises ValidationError: if object has validation errors.
        """

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetrieveUpdateDestroyBoardApiView(BaseRetrieveUpdateDestroyAPIView):
    model = Board
    serializer_class = BoardSerializer


class RetrieveUpdateDestroyTaskApiView(BaseRetrieveUpdateDestroyAPIView):
    model = Task
    serializer_class = TaskSerializer


class CreateBoardApiView(BaseCreateApiView):
    model = Board
    serializer_class = BoardSerializer


class CreateTaskApiView(BaseCreateApiView):
    model = Task
    serializer_class = TaskSerializer


__all__ = [
    'RetrieveUpdateDestroyBoardApiView',
    'CreateBoardApiView',
    'RetrieveUpdateDestroyTaskApiView',
]
