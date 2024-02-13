from datetime import datetime

from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import Serializer, ModelSerializer, StringRelatedField, ListSerializer

from .models import *
from .mixins import CommonValidationMixin


class StatusSerializer(ModelSerializer):
    class Meta:
        model = Status
        fields = ['status']


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['tag']


class PrioritySerializer(ModelSerializer):
    class Meta:
        model = Priority
        fields = ['priority']


class ParticipantsSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class BoardSerializer(ModelSerializer, CommonValidationMixin):

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


class TaskSerializer(ModelSerializer, CommonValidationMixin):

    status = SlugRelatedField(slug_field='status', queryset=Status.objects.all())
    tags = StringRelatedField(many=True, read_only=True)
    priority = StringRelatedField(read_only=True)
    participants = StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Task
        exclude = ['previous_status']

    def validate_status(self, value):

        instance = self.instance
        current_status = instance.status.status

        allowed_transitions = {
            'to_do': ['in_progress'],
            'in_progress': ['done'],
            'done': [],
        }

        if str(value) not in allowed_transitions.get(current_status, []):
            raise ValidationError('Could not change status from %s to %s.' % (current_status, value))

        return value


__all__ = [
    'BoardSerializer',
    'TaskSerializer',
]
