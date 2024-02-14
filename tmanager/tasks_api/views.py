from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import *
from .pagination import ApiViewPaginator
from .serializers import *
from .signals import update_task_history


class BaseRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    serializer_class = None
    model = None
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

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
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        """
        Updates object by Its unique identifier.
            :param request: HTTP PUT request.
            :returns Response: REST API response.
            :raises ValidationError: if object has validation errors.
        """
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
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

    def put(self, request, *args, **kwargs):
        """
        Updates task by Its unique identifier.
            :param request: HTTP PUT request.
            :returns Response: REST API response.
            :raises Validation or Permission error.
        """
        instance = self.get_object()
        if instance.participants.filter(id=request.user.id).exists() or request.user.is_staff:
            serializer = self.serializer_class(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            update_task_history(self.model, instance, False, user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Only participants or staff can change task status.'},
                status=status.HTTP_403_FORBIDDEN,
            )


class CreateBoardApiView(BaseCreateApiView):
    model = Board
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class CreateTaskApiView(BaseCreateApiView):
    model = Task
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class BoardTasksApiView(ListAPIView):

    model = Board
    serializer_class = TaskSerializer
    pagination_class = ApiViewPaginator
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'priority']

    def get_queryset(self):
        return Task.objects.all()

    def get_object(self):
        queryset = Board.objects.all()
        pk = self.kwargs.get(self.lookup_field)
        obj = get_object_or_404(queryset, pk=pk)
        return obj

    def get(self, request, *args, **kwargs):
        """
        Retrieves all task connected with specified board.
            :param request: HTTP POST request.
            :returns Response: REST API response.
        """

        instance = self.get_object()
        queryset = instance.tasks.all()
        filtered_queryset = self.filter_queryset(queryset)

        start = self.request.query_params.get('start')
        end = self.request.query_params.get('end')

        if start:
            filtered_queryset = filtered_queryset.filter(created_at__gte=start)
        if end:
            filtered_queryset = filtered_queryset.filter(created_at__lte=end)

        page = self.paginate_queryset(filtered_queryset)

        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(filtered_queryset, many=True)
        return Response(serializer.data)


class UserRegistrationApiView(CreateAPIView):

    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


__all__ = [
    'RetrieveUpdateDestroyBoardApiView',
    'CreateBoardApiView',
    'CreateTaskApiView',
    'RetrieveUpdateDestroyTaskApiView',
    'BoardTasksApiView',
    'UserRegistrationApiView',
]
