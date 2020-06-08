from rest_framework import serializers
from app.models import *


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class PointDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = PointDetail
        exclude = ['node']


class NodeDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = NodeDetail
        exclude = ['node']


class NodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Node
        exclude = ['graph']


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        exclude = ['graph']


class GraphSerializer(serializers.ModelSerializer):

    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    modified_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    # user_id = serializers.ReadOnlyField(source='user.id')
    # user_id = serializers.IntegerField()
    # username = serializers.CharField(source='user')

    class Meta:
        model = Graph
        fields = '__all__'
        # fields = ('id', 'project_name', 'owner', 'create_time', 'modified_time', 'user_id')
        # exclude = ['user']


class EdgeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Edge
        exclude = ['graph']


class NodeTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeTemplate
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
