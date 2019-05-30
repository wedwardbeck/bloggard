from rest_framework import serializers
from . import models


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'title', 'content', 'created_on', 'created_by', 'updated_on',)
        model = models.Post
