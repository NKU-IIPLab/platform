import json
import os

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import status
from rest_framework.response import Response

from app.models import Graph, Node, NodeDetail, PointDetail, Edge, Channel, File, NodeTemplate, Category
from app.serializers import GraphSerializer, NodeSerializer, NodeDetailSerializer, PointDetailSerializer, EdgeSerializer
from flow_backend import settings


class NE:

    def __init__(self, raw):

        self.raw = raw
        self.project_name = ''
        self.graph_id = raw['id']
        # 原始的node和edge数据
        self.raw_nodes = self.raw['nodes']
        self.raw_edges = self.raw['edges']
        # node_id对应node信息的字典
        self.nodes = {u['id']: u for u in self.raw_nodes}
        # edge_id对应edge信息的字典
        self.edges = {u['id']: u for u in self.raw_edges}
        # 入度统计（用于拓扑排序）
        self.in_count = {u['id']: 0 for u in self.raw_nodes}
        # 出度统计（用于拓扑排序）
        self.out_count = {u['id']: 0 for u in self.raw_nodes}
        # 邻接矩阵，node_id 对应 下一个node_id的集合
        self.matrix = {u['id']: set() for u in self.raw_nodes}
        # point_id 对应 point信息（包含输入/出point的id）的字典
        self.point_matrix = {p['id']: p for u in self.nodes.values() for p in u['point_detail']}
        self.reverse_matrix = {u['id']: set() for u in self.raw_nodes}
        # 深度遍历列表
        self.dfs_list = []

        # 初始化图数据
        self.__init()

    # 检验图合法性
    def is_graph_legal(self):

        # 判断回环
        temp_in_count = self.in_count.copy()
        have_in_zero = True
        while have_in_zero:
            have_in_zero = False
            for node_id, out_nodes in self.matrix.items():
                # 存在入度为0的点
                if node_id in temp_in_count and temp_in_count[node_id] == 0:
                    # 删除该点以及该点的出边
                    del temp_in_count[node_id]
                    for should_minus_one in self.matrix[node_id]:
                        temp_in_count[should_minus_one] = temp_in_count[should_minus_one] - 1
                    have_in_zero = True
                    break
        if len(temp_in_count):
            print('Loop Graph!')
            return False

        # 判断连通性
        if len(self.nodes) != 0:
            node_id_with_zero_in = list(self.in_count.keys())[list(self.in_count.values()).index(0)]
            self.__dfs(node_id_with_zero_in)
            for node_id in self.nodes.keys():
                if node_id not in self.dfs_list:
                    print('Unconnected Graph!')
                    return False
        return True

    def create(self, project_name, owner):
        if not self.is_graph_legal():
            return False

        # 创建新graph
        graph = Graph(project_name=project_name, owner=owner)
        graph.save()
        graph_id = graph.id

        # 创建node
        node_id_to_id = {}
        for node_id in self.dfs_list:
            node = self.nodes[node_id]

            node_obj = Node(node_id=node_id, name=node['name'], raw_script_name=node['raw_script_name'],
                            type=node['type'], shape=node['shape'],
                            size=str(node['size']), color=node['color'],
                            status=node['status'] if 'status' in node else 'init',
                            x=node['x'], y=node['y'], graph_id=graph_id, template_id=node['template_id'])
            node_obj.save()
            node_id_to_id[node_id] = node_obj.id
            for n_detail in node['node_detail']:
                NodeDetail(type=n_detail['type'], name=n_detail['name'], label=n_detail['label'],
                           value=json.dumps({'value': n_detail['value']}),
                           node_id=node_id_to_id[node_id], graph_id=graph_id).save()
            for p_detail in node['point_detail']:
                p_detail_name = p_detail['name'] if 'name' in p_detail.keys() else None
                PointDetail(point_id=p_detail['id'], name=p_detail_name, type=p_detail['type'],
                            proportion=p_detail['proportion'],
                            node_id=node_id_to_id[node_id], graph_id=graph_id).save()

        # 创建edge
        for edge in self.edges.values():
            Edge(edge_id=edge['id'], source=edge['source'], target=edge['target'], start=json.dumps(edge['start']),
                 end=json.dumps(edge['end']),
                 start_point_id=edge['startPointId'], end_point_id=edge['endPointId'],
                 start_point=json.dumps(edge['startPoint']),
                 end_point=json.dumps(edge['endPoint']), shape=edge['shape'], type=edge['type'],
                 source_node_id=node_id_to_id[edge['source']],
                 target_node_id=node_id_to_id[edge['source']], graph_id=graph_id).save()

        return True

    def update(self):
        if not self.is_graph_legal():
            return False

        # 对node更新
        now_stored_nodes = []
        node_id_to_id = {}
        for stored_node in Node.objects.filter(graph_id=self.graph_id):
            node_id = stored_node.node_id
            node_did = stored_node.id
            should_update = False
            for node in self.nodes.values():
                if 'did' in node and node_did == node['did']:
                    should_update = True
            if should_update:
                # 更新其他节点
                node_id_to_id[node_id] = stored_node.id
                now_stored_nodes.append(node_id)
                node = self.nodes[node_id]
                Node.objects.filter(node_id=node_id, graph_id=self.graph_id) \
                    .update(node_id=node_id, template_id=node['template_id'], name=node['name'],
                            raw_script_name=node['raw_script_name'],
                            type=node['type'], shape=node['shape'],
                            size=str(node['size']), color=node['color'],
                            status=node['status'] if 'status' in node else 'init', x=node['x'], y=node['y'])
                # 更新node_detail
                for n_detail in node['node_detail']:
                    NodeDetail.objects.filter(id=n_detail['id']) \
                        .update(type=n_detail['type'], name=n_detail['name'],
                                label=n_detail['label'],
                                value=json.dumps({'value': n_detail['value']}),
                                node_id=stored_node.id)
                # 更新point_detail
                for p_detail in node['point_detail']:
                    p_detail_name = p_detail['name'] if 'name' in p_detail.keys() else None
                    PointDetail.objects.filter(point_id=p_detail['id'], node_id=stored_node.id, graph_id=self.graph_id) \
                        .update(point_id=p_detail['id'], name=p_detail_name, type=p_detail['type'],
                                proportion=p_detail['proportion'],
                                node_id=stored_node.id)
            else:
                # 删除更新后不存在的节点
                stored_node.delete()

        for node in self.nodes.values():
            if 'did' not in node.keys():
                node_id = node['id']
                # 创建新节点
                node = self.nodes[node_id]
                node_obj = Node(node_id=node_id, name=node['name'], raw_script_name=node['raw_script_name'],
                                type=node['type'], shape=node['shape'],
                                size=str(node['size']), color=node['color'],
                                status=node['status'] if 'status' in node else 'init',
                                x=node['x'], y=node['y'], graph_id=self.graph_id, template_id=node['template_id'])
                node_obj.save()
                node_id_to_id[node_id] = node_obj.id
                for n_detail in node['node_detail']:
                    NodeDetail(type=n_detail['type'], name=n_detail['name'], label=n_detail['label'],
                               value=json.dumps({'value': n_detail['value']}),
                               node_id=node_id_to_id[node_id], graph_id=self.graph_id).save()
                for p_detail in node['point_detail']:
                    p_detail_name = p_detail['name'] if 'name' in p_detail.keys() else None
                    PointDetail(point_id=p_detail['id'], name=p_detail_name, type=p_detail['type'],
                                proportion=p_detail['proportion'],
                                node_id=node_id_to_id[node_id], graph_id=self.graph_id).save()

        # 对edge更新
        now_stored_edges = []
        for stored_edge in Edge.objects.filter(graph_id=self.graph_id):
            edge_id = stored_edge.edge_id
            edge_did = stored_edge.id
            should_update = False
            for edge in self.edges.values():
                if 'did' in edge and edge_did == edge['did']:
                    should_update = True
            if should_update:
                now_stored_edges.append(edge_id)
                edge = self.edges[edge_id]
                Edge.objects.filter(edge_id=edge_id, graph_id=self.graph_id) \
                    .update(source=edge['source'], target=edge['target'],
                            start=json.dumps(edge['start']),
                            end=json.dumps(edge['end']),
                            start_point_id=edge['startPointId'], end_point_id=edge['endPointId'],
                            start_point=json.dumps(edge['startPoint']),
                            end_point=json.dumps(edge['endPoint']), shape=edge['shape'], type=edge['type'],
                            source_node_id=node_id_to_id[edge['source']],
                            target_node_id=node_id_to_id[edge['source']], graph_id=self.graph_id)
            else:
                stored_edge.delete()

        for edge in self.edges.values():
            if 'did' not in edge.keys():
                edge_id = edge['id']
                # 创建新edge
                edge = self.edges[edge_id]
                Edge(edge_id=edge['id'], source=edge['source'], target=edge['target'], start=json.dumps(edge['start']),
                     end=json.dumps(edge['end']),
                     start_point_id=edge['startPointId'], end_point_id=edge['endPointId'],
                     start_point=json.dumps(edge['startPoint']),
                     end_point=json.dumps(edge['endPoint']), shape=edge['shape'], type=edge['type'],
                     source_node_id=node_id_to_id[edge['source']],
                     target_node_id=node_id_to_id[edge['source']], graph_id=self.graph_id).save()

        return True

    @staticmethod
    def list(graph, graph_id):
        # 对node遍历
        node_data = NodeSerializer(Node.objects.filter(graph_id=graph_id), many=True).data
        for node in node_data:
            # 对node_detail遍历
            node_detail_data = NodeDetailSerializer(NodeDetail.objects.filter(node_id=node['id']), many=True).data
            for node_detail in node_detail_data:
                node_detail['value'] = json.loads(node_detail['value'])['value']
                # del node_detail['id']

            # 对point_detail遍历
            point_detail_data = PointDetailSerializer(PointDetail.objects.filter(node_id=node['id']), many=True).data
            for point_detail in point_detail_data:
                point_detail['id'] = point_detail['point_id']
                del point_detail['point_id']

            # 整理node
            node['did'] = node['id']
            node['id'] = node['node_id']
            node['size'] = json.loads(node['size'])
            node['template_id'] = node.pop('template')
            del node['node_id']
            node['node_detail'] = node_detail_data
            node['point_detail'] = point_detail_data

        # 对edge遍历
        edge_data = EdgeSerializer(Edge.objects.filter(graph_id=graph_id), many=True).data
        for edge in edge_data:
            edge['did'] = edge['id']
            edge['id'] = edge.pop('edge_id')
            edge['start'] = json.loads(edge['start'])
            edge['end'] = json.loads(edge['end'])
            edge['startPointId'] = edge.pop('start_point_id')
            edge['endPointId'] = edge.pop('end_point_id')
            edge['startPoint'] = json.loads(edge.pop('start_point'))
            edge['endPoint'] = json.loads(edge.pop('end_point'))
        graph['nodes'] = node_data
        graph['edges'] = edge_data

        return graph

    def run_node(self, graph_id, node_id, user, is_project=False):

        if not is_project:
            Graph.objects.filter(id=graph_id).update(status='loading')

        node = self.nodes[node_id]
        if node['raw_script_name']:
            script_path = os.path.join(settings.MEDIA_ROOT, self.project_name, 'script', node_id + '.py')
            # 设置数据库中 node 的状态为 loading
            Node.objects.filter(node_id=node_id, graph_id=self.graph_id).update(status='loading')
            # 通过websocket发送状态给前端
            receiver_channel = Channel.objects.get(user=user)
            if receiver_channel is not None:
                async_to_sync(get_channel_layer().send)(receiver_channel.channel_name, {
                    'type': 'send_status',
                    'msg': {
                        'nodeId': node_id,
                        'status': 'loading'
                    }
                })
            # 运行脚本
            os.system(f'python {script_path}')

            # 设置数据库中 node 的状态为 complete
            Node.objects.filter(node_id=node_id, graph_id=self.graph_id).update(status='complete')
            # 通过websocket发送状态给前端
            receiver_channel = Channel.objects.get(user=user)
            if receiver_channel is not None:
                async_to_sync(get_channel_layer().send)(receiver_channel.channel_name, {
                    'type': 'send_status',
                    'msg': {
                        'nodeId': node_id,
                        'status': 'complete'
                    }
                })
        if not is_project:
            receiver_channel = Channel.objects.get(user=user)
            Graph.objects.filter(id=graph_id).update(status='complete')
            if receiver_channel is not None:
                async_to_sync(get_channel_layer().send)(receiver_channel.channel_name, {
                    'type': 'send_status',
                    'msg': 'complete'
                })

    # todo 运行脚本 加入websocket与前端通信
    def run_script(self, graph_id, user):

        # 更新数据库graph状态
        Graph.objects.filter(id=graph_id).update(status='loading')

        for node_id in self.dfs_list:
            self.run_node(graph_id, node_id, user, True)

        # 运行结束，通过websocket发送成功
        receiver_channel = Channel.objects.get(user=user)
        Graph.objects.filter(id=graph_id).update(status='complete')
        if receiver_channel is not None:
            async_to_sync(get_channel_layer().send)(receiver_channel.channel_name, {
                'type': 'send_status',
                'msg': 'complete'
            })

    # todo 生成脚本
    def generate_script(self):
        self.project_name = Graph.objects.get(id=self.graph_id).project_name
        for node_id in self.dfs_list:
            node = self.nodes[node_id]
            node_details = {node_detail['name']: node_detail for node_detail in node['node_detail']}
            point_details = {p['id']: self.point_matrix[p['id']] for p in node['point_detail']}
            # 针对 upload 和 其他类型的node做不同处理
            # 1）每一个结点都根据raw_script_name去app/utils/raw_scripts目录下找相应的原始脚本
            # 2）根据node_detail中的name和value进行脚本字符串的替换
            # 3）根据point_detail中的id和target分别设置为 in_path 和 out_path
            # 4）特殊的，对于upload结点的value和in_path要做特殊处理（upload结点的in_path为node_detail中的upload value）
            if 'selectFile' in node_details.keys():
                # 对于 upload 结点，需要特殊的in_path
                fid = node_details['selectFile']['value']
                filepath = File.objects.get(id=fid).filepath
                filepath = os.path.join(settings.MEDIA_ROOT, filepath)
                params = {'in_path': repr(filepath)}
                # 生成in_path out_path
                out_index = 1
                for point_id, point in point_details.items():
                    params[f'out_path_{point["name"]}'] = repr(
                        os.path.join(settings.MEDIA_ROOT, self.project_name, 'result', point_id))
                    out_index += 1
            else:
                params = {}
                in_index = 1
                out_index = 1
                # 生成in_path out_path
                for point_id, point in point_details.items():
                    if point['type'] == 'output':
                        params[f'out_path_{point["name"]}'] = repr(
                            os.path.join(settings.MEDIA_ROOT, self.project_name, 'result', point_id))
                        out_index += 1
                    elif point['type'] == 'input':
                        params[f'in_path_{point["name"]}'] = repr(
                            os.path.join(settings.MEDIA_ROOT, self.project_name, 'result',
                                         self.point_matrix[point_id]['target']))
                # 对node_detail生成替换
                for node_name, node_detail in node_details.items():
                    if node_name != 'name':
                        params[node_name] = \
                            repr(node_detail['value']) if node_detail['type'] == 'input' else node_detail['value']
            if node['raw_script_name']:
                category_name = Category.objects.filter(nodetemplate__node__node_id=node_id,
                                                        nodetemplate__node__graph_id=self.graph_id).first().name
                self.__generate_script(category_name, node['raw_script_name'], node_id, **params)

    def __generate_script(self, category_name, raw_script_name, node_id, **kwargs):
        raw_script_path = os.path.join(settings.UTIL_ROOT, 'raw_scripts', category_name, raw_script_name)
        with open(raw_script_path, 'r', encoding='utf-8') as in_f:
            script = in_f.read() % kwargs
            with open(os.path.join(settings.MEDIA_ROOT, self.project_name, 'script', node_id + '.py'), 'w',
                      encoding='utf-8') as out_f:
                out_f.write(script)
                in_f.close()
                out_f.close()

    def __init(self):
        for edge in self.edges.values():
            start_node_id = edge['source']
            end_node_id = edge['target']
            start_point_id = edge['startPointId']
            end_point_id = edge['endPointId']
            self.in_count[end_node_id] = self.in_count[end_node_id] + 1
            self.out_count[start_node_id] = self.out_count[start_node_id] + 1
            self.matrix[start_node_id].add(end_node_id)
            self.reverse_matrix[end_node_id].add(start_node_id)
            self.point_matrix[start_point_id]['target'] = end_point_id
            self.point_matrix[end_point_id]['target'] = start_point_id

    def __dfs(self, node_id: str):
        if node_id not in self.dfs_list:
            self.dfs_list.append(node_id)

        out_nodes = self.matrix[node_id]
        for node in out_nodes:
            if node not in self.dfs_list:
                self.dfs_list.append(node)
                self.__dfs(node)


if __name__ == '__main__':
    from Media.templates.project_json import *

    ne = NE(k_means_json)
    ne.is_graph_legal()
    ne.generate_script(1)
