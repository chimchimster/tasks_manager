from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import *

app_name = 'tasks_api'

schema_view = get_schema_view(
   openapi.Info(
      title="NCRM Group",
      default_version='v1',
      description="Task manager REST API using DRF.",
   ),
   public=True,
)


urlpatterns = [

    # JWT TOKENS
    path('token/get/', TokenObtainPairView.as_view(), name='token_get'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # GET, PUT, DELETE methods
    path('board/<int:pk>/', RetrieveUpdateDestroyBoardApiView.as_view(), name='board'),
    path('task/<int:pk>/', RetrieveUpdateDestroyTaskApiView.as_view(), name='task'),
    path('board/<int:pk>/tasks/', BoardTasksApiView.as_view(), name='board_tasks'),

    # POST methods
    path('board/create/', CreateBoardApiView.as_view(), name='create_board'),
    path('task/create/', CreateTaskApiView.as_view(), name='create_task'),
    path('register/', UserRegistrationApiView.as_view(), name='user-register'),

    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]