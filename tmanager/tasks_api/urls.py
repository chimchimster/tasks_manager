from django.urls import path

from .views import *

app_name = 'tasks_api'

urlpatterns = [

    # GET methods
    path('board/<int:pk>/', RetrieveUpdateDestroyBoardApiView.as_view(), name='retrieve_board'),

    # UPDATE methods
    path('board/<int:pk>/', RetrieveUpdateDestroyBoardApiView.as_view(), name='update_board'),

    # POST methods
    path('board/create/', CreateBoardApiView.as_view(), name='create_board'),
]