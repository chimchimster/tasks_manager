from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import *

app_name = 'tasks_api'

urlpatterns = [

    # JWT TOKENS
    path('token/get/', TokenObtainPairView.as_view(), name='token_get'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # GET, PUT, DELETE methods
    path('board/<int:pk>/', RetrieveUpdateDestroyBoardApiView.as_view(), name='board'),
    path('task/<int:pk>/', RetrieveUpdateDestroyTaskApiView.as_view(), name='task'),

    # POST methods
    path('board/create/', CreateBoardApiView.as_view(), name='create_board'),
]