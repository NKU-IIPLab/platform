import json
import os
import threading
import pandas as pd
import numpy as np

from django.http import FileResponse
from django.utils.http import urlquote
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import PointDetail, Edge, Graph, File, NodeTemplate, Category
from app.serializers import FileSerializer
from app.utils.algorithm import NE
from flow_backend import settings


@api_view(['GET', 'POST'])
def handle_output(request):
    if request.method == 'POST':
        data = request.data
        return Response({'data': 'success'}, status=status.HTTP_201_CREATED)
    elif request.method == 'GET':
        return Response({'data': 'success'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def is_preview_valid(request):
    node_id = request.GET['nodeId']
    graph_id = request.GET['graphId']

    graph = Graph.objects.get(id=graph_id)
    project_name = graph.project_name
    point_details = PointDetail.objects.filter(node__node_id=node_id, graph_id=graph_id)
    point_id = ''
    for point_detail in point_details:
        if point_detail.type == 'input':
            point_id = point_detail.point_id
            break
    edge = Edge.objects.filter(end_point_id=point_id, graph_id=graph_id).first()
    if edge is None:
        return Response({'data': False}, status.HTTP_202_ACCEPTED)
    start_point_id = edge.start_point_id
    filepath = os.path.join(settings.MEDIA_ROOT, project_name, 'result', start_point_id)
    if os.path.exists(filepath):
        return Response({'data': True}, status.HTTP_202_ACCEPTED)
    else:
        return Response({'data': False}, status.HTTP_202_ACCEPTED)


@api_view(['GET'])
def preview_csv(request):
    node_id = request.GET['nodeId']
    graph_id = request.GET['graphId']
    transit = request.GET['transit'] if 'transit' in request.GET else False

    graph = Graph.objects.get(id=graph_id)
    project_name = graph.project_name
    point_details = PointDetail.objects.filter(node__node_id=node_id, graph_id=graph_id)
    point_id = ''
    for point_detail in point_details:
        if point_detail.type == 'input':
            point_id = point_detail.point_id
            break
    edge = Edge.objects.get(end_point_id=point_id, graph_id=graph_id)
    start_point_id = edge.start_point_id
    filepath = os.path.join(settings.MEDIA_ROOT, project_name, 'result', start_point_id)
    if os.path.exists(filepath):
        count = 1
        for count, line in enumerate(
                open(filepath, 'r', encoding='utf-8')):
            count += 1

        data = pd.read_csv(filepath, nrows=10, header=None)
        val1 = data.values

        if count >= 11:

            data1 = pd.read_csv(filepath, skiprows=count - 2, nrows=count, header=None)
            val2 = data1.values

            index = np.append(np.arange(1, val1.shape[0] + 1), ['...'])
            index = np.append(index, np.arange(count - 1, count + 1))

            data3 = pd.concat([data, pd.DataFrame([['...'] * data.shape[1]]), data1], ignore_index=True)
        else:
            index = np.arange(1, val1.shape[0] + 1)
            data3 = data
        # val3 = np.r_[val1, [['...'] * val1.shape[1]], val2]
        return Response({'pid': start_point_id, 'index': index, 'data': data3.values.T if transit else data3.values},
                        status.HTTP_202_ACCEPTED)
    else:
        return Response({'data': '文件不存在'}, status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def preview_echarts(request):
    queries = request.GET.getlist('queries[]')
    point_id = request.GET['pid']
    graph_id = request.GET['graphId']

    graph = Graph.objects.get(id=graph_id)
    project_name = graph.project_name
    filepath = os.path.join(settings.MEDIA_ROOT, project_name, 'result', point_id)

    csv = pd.read_csv(filepath, header=None)
    data = {}
    for query in queries:
        data[query] = csv[int(query) - 1].values

    return Response({'data': data}, status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def is_filename_valid(request):
    if request.method == 'POST':
        filename = request.data['filename']
        graph_id = request.data['graphId']
        f_obj = File.objects.filter(name=filename, graph_id=graph_id)
        is_valid = len(f_obj) != 0 and os.path.exists(
            os.path.join(settings.MEDIA_ROOT, f_obj[0].filepath)) and os.path.isfile(
            os.path.join(settings.MEDIA_ROOT, f_obj[0].filepath))
        return Response({'data': is_valid}, status.HTTP_201_CREATED)


@api_view(['PUT'])
def run_node(request):
    user = request.user
    graph_json = json.loads(request.data['graph'])
    node_id = request.data['nodeId']
    graph = NE(graph_json)
    graph_id = graph_json['id']

    if graph_id is None:
        if not graph.create('k-means', 'christ'):
            return Response({'data': '流程图存在错误，请检查'}, status.HTTP_406_NOT_ACCEPTABLE)
    else:
        graph.project_name = Graph.objects.get(id=graph_id).project_name
        if not graph.update():
            return Response({'data': '流程图存在错误，请检查'}, status.HTTP_406_NOT_ACCEPTABLE)

    # 检查是否可以运行
    project_name = graph.project_name
    point_details = PointDetail.objects.filter(node__node_id=node_id, graph_id=graph_id)
    for point_detail in point_details:
        if point_detail.type == 'input':
            point_id = point_detail.point_id
            edge = Edge.objects.get(end_point_id=point_id, graph_id=graph_id)
            start_point_id = edge.start_point_id
            filepath = os.path.join(settings.MEDIA_ROOT, project_name, 'result', start_point_id)
            if not os.path.exists(filepath):
                return Response({'data': '节点当前不可运行'}, status.HTTP_406_NOT_ACCEPTABLE)

    # 生成脚本
    graph.generate_script()

    # 新线程运行
    threading.Thread(target=graph.run_node, args=[graph_id, node_id, user]).start()

    return Response({'data': 'success'}, status.HTTP_200_OK)


@api_view(['PUT'])
def run_project(request):
    user = request.user
    graph_json = json.loads(request.data['graph'])
    graph = NE(graph_json)
    graph.project_name = 'k-means'
    graph_id = graph_json['id'] if 'id' in graph_json else None

    if graph_id is None:
        if not graph.create('k-means', 'christ'):
            return Response({'data': '流程图存在错误，请检查'}, status.HTTP_406_NOT_ACCEPTABLE)
    else:
        if not graph.update():
            return Response({'data': '流程图存在错误，请检查'}, status.HTTP_406_NOT_ACCEPTABLE)

    # 生成脚本
    graph.generate_script()
    # 新线程运行
    threading.Thread(target=graph.run_script, args=[graph_id, user]).start()

    return Response({'data': 'success'}, status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def project_file_list(request):
    graph_id = request.GET['graphId']
    graph = Graph.objects.get(id=graph_id)
    file_list = FileSerializer(File.objects.filter(graph=graph), many=True).data
    # project_name = graph.project_name
    #
    # path = f'{settings.MEDIA_ROOT}\\{project_name}\\upload\\'
    return Response({'data': file_list}, status.HTTP_200_OK)


@api_view(['post'])
@permission_classes([IsAuthenticated])
def create_node(request):
    data = request.data
    category_id = data['selectCategory']
    NodeTemplate(category_id=category_id, node_detail=json.dumps(data['nodeDetails']),
                 point_detail=json.dumps(data['pointDetails']),
                 raw_script_name=data['raw_script_name'], shape=data['shape'], size=data['size'],
                 color=data['color'], name=data['name']).save()

    return Response(status=status.HTTP_201_CREATED)
