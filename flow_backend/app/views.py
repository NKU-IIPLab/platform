import json
import os
import shutil
from datetime import datetime

from django.http import FileResponse
from django.utils.http import urlquote
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import *
from app.serializers import CategorySerializer, GraphSerializer, NodeTemplateSerializer, FileSerializer
from app.utils.algorithm import NE
from flow_backend import settings


class CustomPagination(PageNumberPagination):
    # 指定每一页的个数，默认为配置文件里面的PAGE_SIZE
    page_size = 10

    # 可以让前端指定每页个数，默认为空，这里指定page_size去指定显示个数
    page_size_query_param = 'page_size'

    # 可以让前端指定页码数，默认就是page参数去接收
    page_query_param = 'page'

    def get_paginated_response(self, data):
        from collections import OrderedDict
        return Response(OrderedDict([('count', self.page.paginator.count), ('res', data)]))


class NodeTemplateViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = NodeTemplate.objects.all()

    def list(self, request, *args, **kwargs):
        category = Category.objects.all()

        categories = CategorySerializer(category, many=True).data
        for category in categories:
            node_templates = NodeTemplateSerializer(NodeTemplate.objects.filter(category_id=category['id']),
                                                    many=True).data
            for node_template in node_templates:
                node_template['node_detail'] = json.loads(node_template['node_detail'])
                node_template['point_detail'] = json.loads(node_template['point_detail'])
            category['children'] = node_templates
            category['is_menu'] = True
        return Response({'data': categories}, status=status.HTTP_201_CREATED)


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()

    def list(self, request, *args, **kwargs):
        category = Category.objects.all()
        categories = CategorySerializer(category, many=True).data

        return Response({'data': categories}, status=status.HTTP_201_CREATED)


class GraphViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Graph.objects.all()
    serializer_class = GraphSerializer

    @action(methods=['put'], detail=False)
    def put(self, request):
        graph_json = json.loads(request.data['graph'])
        graph = NE(graph_json)
        graph_id = graph_json['id'] if 'id' in graph_json else None

        # 检验用户是否有权访问该graph
        self.queryset = self.queryset.filter(id=graph_id).first()
        graph_obj = GraphSerializer(self.queryset).data
        if graph_obj['user'] != self.request.user.id:
            return Response({'data': '无法访问他人作业'}, status.HTTP_403_FORBIDDEN)

        if graph_id is None:
            return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            if graph.update():
                Graph.objects.filter(id=graph_id).update(modified_time=datetime.now())
                return Response({'data': 'success'}, status.HTTP_201_CREATED)
            else:
                return Response({'data': '流程图存在错误，请检查'}, status.HTTP_406_NOT_ACCEPTABLE)

    def list(self, request, *args, **kwargs):

        user = request.user
        graph_id = self.request.query_params.get('graphId', None)
        if graph_id is not None:
            self.queryset = self.queryset.filter(id=graph_id).first()
            graph = GraphSerializer(self.queryset).data
            # 检验用户是否有权访问该graph
            if graph['user'] == user.id or user.username == 'admin':
                return Response({'data': NE.list(graph, graph_id)}, status=status.HTTP_201_CREATED)
            else:
                return Response({'data': '无法访问他人作业'}, status.HTTP_403_FORBIDDEN)
        else:
            if user.username == 'admin':
                self.queryset = self.queryset.filter()
            else:
                self.queryset = self.queryset.filter(user=user)
            pagination_class = CustomPagination()
            page_query = pagination_class.paginate_queryset(queryset=self.queryset, request=request, view=self)
            serializer = GraphSerializer(page_query, many=True)
            graph = pagination_class.get_paginated_response(serializer.data)
            return graph

    @action(methods=['delete'], detail=False)
    def multiple_delete(self, instance):
        project_ids = self.request.query_params.getlist('projectIds[]', None)
        graphs = Graph.objects.filter(id__in=project_ids)

        for graph in graphs:
            if self.request.user.id != graph.user.id:
                return Response({'data': '无法删除他人作业'}, status=status.HTTP_403_FORBIDDEN)

        for graph in graphs:
            project_name = graph.project_name
            dir_path = os.path.join(settings.MEDIA_ROOT, project_name)
            shutil.rmtree(dir_path)

        graphs.delete()

        return Response({'data': 'success'}, status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        project_name = self.request.data['projectName']
        owner = user.username
        create_time = datetime.now()
        modified_time = datetime.now()

        if len(Graph.objects.filter(project_name=project_name, user=user)) != 0:
            return Response({'data': '项目名已存在'}, status=status.HTTP_403_FORBIDDEN)

        Graph(project_name=project_name, owner=owner, create_time=create_time, modified_time=modified_time,
              status='init', user=user).save()

        # 创建项目文件夹
        dir_path = os.path.join(settings.MEDIA_ROOT, project_name)
        result_path = os.path.join(dir_path, 'result')
        script_path = os.path.join(dir_path, 'script')
        upload_path = os.path.join(dir_path, 'upload')

        os.mkdir(dir_path)
        os.mkdir(result_path)
        os.mkdir(script_path)
        os.mkdir(upload_path)

        return Response({'data': 'success'}, status=status.HTTP_201_CREATED)


class ScriptView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES['file']
        filename = request.POST['filename']
        category_id = request.POST['selectCategory']

        category_name = Category.objects.get(id=category_id).name

        dir_path = os.path.join(settings.UTIL_ROOT, 'raw_scripts', category_name)
        file_path = os.path.join(dir_path, filename)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        with open(file_path, 'wb+') as des:
            for chunk in file_obj.chunks():
                des.write(chunk)

        return Response({'data': 'success'}, status.HTTP_201_CREATED)


class UploadFileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES['file']
        filename = file_obj.name
        graph_id = request.POST['graphId']
        graph = Graph.objects.get(id=graph_id)

        project_name = graph.project_name
        dir_path = os.path.join(settings.MEDIA_ROOT, project_name, 'upload')
        file_path = os.path.join(dir_path, filename)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        f_obj = File.objects.filter(graph_id=graph_id, name=filename).first()
        if f_obj is not None:
            # 更新数据库 size, filepath 字段
            f_obj.size = file_obj.size
            f_obj.filepath = os.path.join(project_name, 'upload', filename)
            f_obj.save()
        else:
            # 写入数据库
            f_obj = File(name=filename, status='success', size=file_obj.size, percentage=100,
                         filepath=os.path.join(project_name, 'upload', filename), graph_id=graph_id)
            f_obj.save()

        with open(file_path, 'wb+') as des:
            for chunk in file_obj.chunks():
                des.write(chunk)

        file_list = FileSerializer(File.objects.filter(graph_id=graph_id), many=True).data
        return Response({'data': file_list}, status.HTTP_201_CREATED)

    def get(self, request):
        graph_id = request.GET['graphId']
        node_id = request.GET['nodeId']

        graph = Graph.objects.get(id=graph_id)
        project_name = graph.project_name

        point_detail = PointDetail.objects.get(node__node_id=node_id, graph_id=graph_id)
        point_id = point_detail.point_id

        edge = Edge.objects.get(end_point_id=point_id, graph_id=graph_id)
        start_point_id = edge.start_point_id

        file = open(os.path.join(settings.MEDIA_ROOT, project_name, 'result', start_point_id), 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        name = project_name

        response['Content-Disposition'] = 'attachment;filename="%s.txt"' % (urlquote(name))
        return response

    def delete(self, request):
        fid = request.query_params.get('id', None)
        file = File.objects.get(id=fid)
        filepath = os.path.join(settings.MEDIA_ROOT, file.filepath)
        if file is not None and os.path.exists(filepath) and os.path.isfile(filepath):
            graph_id = file.graph_id
            os.remove(filepath)
            file.delete()

            file_list = FileSerializer(File.objects.filter(graph_id=graph_id), many=True).data
            return Response({'data': file_list}, status.HTTP_201_CREATED)
        else:
            return Response({'data': '文件不存在'}, status.HTTP_404_NOT_FOUND)
