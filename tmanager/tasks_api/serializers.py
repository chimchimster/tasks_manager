from datetime import datetime

from rest_framework.serializers import ModelSerializer

from .models import *
from .mixins import CommonValidationMixin


class BoardSerializer(ModelSerializer, CommonValidationMixin):

    class Meta:
        model = Board
        fields = '__all__'

    def to_representation(self, instance):
        """ Response representation of model. """

        representation = super().to_representation(instance)

        created_at, updated_at = representation.get('created_at'), representation.get('updated_at')

        created_at = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%S.%fZ')
        updated_at = datetime.strptime(updated_at, '%Y-%m-%dT%H:%M:%S.%fZ')

        representation['created_at'] = created_at.strftime('%d-%m-%Y %H:%M:%S')
        representation['updated_at'] = updated_at.strftime('%d-%m-%Y %H:%M:%S')

        return representation


class TaskSerializer(ModelSerializer, CommonValidationMixin):

    class Meta:
        model = Task
        fields = '__all__'


__all__ = [
    'BoardSerializer',
    'TaskSerializer',
]