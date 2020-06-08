# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models

from app.CustomUserManager import UserManager


class User(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)

    objects = UserManager()
    USERNAME_FIELD = 'username'


class Category(models.Model):
    name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category'


class Channel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'channel'


class Edge(models.Model):
    edge_id = models.CharField(max_length=45, blank=True, null=True)
    source = models.CharField(max_length=45, blank=True, null=True)
    target = models.CharField(max_length=45, blank=True, null=True)
    start = models.TextField(blank=True, null=True)  # This field type is a guess.
    end = models.TextField(blank=True, null=True)  # This field type is a guess.
    start_point_id = models.CharField(max_length=45, blank=True, null=True)
    end_point_id = models.CharField(max_length=45, blank=True, null=True)
    start_point = models.TextField(blank=True, null=True)  # This field type is a guess.
    end_point = models.TextField(blank=True, null=True)  # This field type is a guess.
    shape = models.CharField(max_length=45, blank=True, null=True)
    type = models.CharField(max_length=45, blank=True, null=True)
    source_node = models.ForeignKey('Node', models.DO_NOTHING, related_name='source_node')
    target_node = models.ForeignKey('Node', models.DO_NOTHING, related_name='target_node')
    graph = models.ForeignKey('Graph', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'edge'


class File(models.Model):
    name = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=45, blank=True, null=True)
    size = models.CharField(max_length=45, blank=True, null=True)
    percentage = models.IntegerField(blank=True, null=True)
    filepath = models.TextField(blank=True, null=True)
    graph = models.ForeignKey('Graph', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'file'


class Graph(models.Model):
    project_name = models.CharField(max_length=120, blank=True, null=True)
    owner = models.CharField(max_length=120, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    modified_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=45, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'graph'


class Node(models.Model):
    node_id = models.CharField(max_length=45, blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    raw_script_name = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=45, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=45, blank=True, null=True)
    shape = models.CharField(max_length=45, blank=True, null=True)
    size = models.CharField(max_length=45, blank=True, null=True)
    color = models.CharField(max_length=45, blank=True, null=True)
    x = models.IntegerField(blank=True, null=True)
    y = models.IntegerField(blank=True, null=True)
    graph = models.ForeignKey(Graph, models.DO_NOTHING)
    template = models.ForeignKey('NodeTemplate', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'node'
        unique_together = (('id', 'graph', 'template'),)


class NodeDetail(models.Model):
    type = models.CharField(max_length=45, blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    label = models.CharField(max_length=45, blank=True, null=True)
    value = models.TextField(blank=True, null=True)
    node = models.ForeignKey(Node, models.DO_NOTHING, related_name='noe_detail_node')
    graph = models.ForeignKey(Node, models.DO_NOTHING, related_name='node_detail_graph')

    class Meta:
        managed = False
        db_table = 'node_detail'


class NodeTemplate(models.Model):
    name = models.CharField(max_length=45, blank=True, null=True)
    raw_script_name = models.TextField(blank=True, null=True)
    shape = models.CharField(max_length=45, blank=True, null=True)
    size = models.CharField(max_length=45, blank=True, null=True)
    color = models.CharField(max_length=45, blank=True, null=True)
    node_detail = models.TextField(blank=True, null=True)  # This field type is a guess.
    point_detail = models.TextField(blank=True, null=True)  # This field type is a guess.
    category = models.ForeignKey(Category, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'node_template'


class PointDetail(models.Model):
    point_id = models.CharField(max_length=45, blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=45, blank=True, null=True)
    proportion = models.FloatField(blank=True, null=True)
    func = models.CharField(max_length=45, blank=True, null=True)
    node = models.ForeignKey(Node, models.DO_NOTHING, related_name='point_detail_node')
    graph = models.ForeignKey(Node, models.DO_NOTHING, related_name='point_detail_graph')

    class Meta:
        managed = False
        db_table = 'point_detail'
