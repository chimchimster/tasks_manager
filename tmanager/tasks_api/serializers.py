from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer, StringRelatedField, PrimaryKeyRelatedField, ManyRelatedField, CharField

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


class ManyRelatedTagField(ManyRelatedField):
    def to_representation(self, value):
        return TagSerializer(value, many=True).data

    def to_internal_value(self, data):
        tags = []
        for tag_data in data:
            tag, created = Tag.objects.get_or_create(**tag_data)
            tags.append(tag)
        return tags


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


class UserSerializer(ModelSerializer):

    password = CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class TaskSerializer(ModelSerializer, CommonValidationMixin):

    status = SlugRelatedField(slug_field='status', queryset=Status.objects.all())
    priority = PrimaryKeyRelatedField(queryset=Priority.objects.all())
    participants = StringRelatedField(many=True, read_only=True)
    tags = StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Task
        exclude = ['previous_status']

    def validate_status(self, value):

        instance = self.instance

        if not instance:
            return value

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
    'UserSerializer',
]
