from datetime import datetime

from rest_framework.serializers import ModelSerializer

from .models import *


class BoardSerializer(ModelSerializer):
    class Meta:
        model = Board
        fields = ['title', 'description', 'created_at', 'updated_at']

    def to_representation(self, instance):

        representation = super().to_representation(instance)

        created_at, updated_at = representation.get('created_at'), representation.get('updated_at')

        created_at = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%S.%fZ')
        updated_at = datetime.strptime(updated_at, '%Y-%m-%dT%H:%M:%S.%fZ')

        representation['created_at'] = created_at.strftime('%d-%m-%Y %H:%M:%S')
        representation['updated_at'] = updated_at.strftime('%d-%m-%Y %H:%M:%S')

        return representation


__all__ = [
    'BoardSerializer',
]