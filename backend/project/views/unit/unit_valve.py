from django.db.models import Q

from project.views.unit.unit import UnitCommonViewSet
from project.serializers.unit import (
    RVValveSerializer,
    EDUHLValveSerializer,
    EDUValveSerializer,
    ValveListSerializer
)
from project.models import Valve
from dvadmin.utils.json_response import DetailResponse, SuccessResponse, ErrorResponse


class ValveViewSet(UnitCommonViewSet):
    """
    调整阀增删改查接口
    """
    MODEL = Valve
    
    # swagger_fake_view = True
    
    def get_matching_serializer(self, mode, high_low):
        serializer = None
        if mode == 1:  # EDU(BDV)
            if high_low:  # High/Low为True
                serializer = EDUHLValveSerializer
            else:  # High/Low为False
                serializer = EDUValveSerializer
        elif mode == 0:  # RV
            serializer = RVValveSerializer

        print("valve serializer is", serializer)
        return serializer

    def list(self, request, *args, **kwargs):
        query_param = request.query_params.get("mode", "")
        search = request.query_params.get("search", None)  # 模糊搜索值
        if query_param != "":
            if (i := int(query_param)) in range(len(Valve.MODE)):
                q = bq = Q(mode=i)
                if not request.user.is_superuser:
                    q = Q(is_global=True) | Q(creator=request.user)
                    if pid := request.query_params.get("project", None):
                        q = q | Q(project=pid)
                    q = q & bq
                if search:
                    q = q & Q(item__icontains=search)
                queryset = Valve.objects.filter(q)[:self.LIMIT]
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = ValveListSerializer(page, many=True, request=request)
                    return self.get_paginated_response(serializer.data)
                serializer = ValveListSerializer(queryset, many=True, request=request)
                return SuccessResponse(data=serializer.data, msg="获取成功", total=queryset.count())

            else:
                return ErrorResponse(msg="The mode '%s' is not exists." % i)

        else:
            return ErrorResponse(msg="The 'mode' parameter must be passed.")

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        # 如果project给了个''
        if data.get("project", "") == "":
            data.pop("project", None)
        data.pop("is_global", None)  # 项目里没法创建全局部件

        mode = data.get("mode", "")
        if mode != "":
            # 不是超管不能创建全局部件
            # if int(data.get("is_global")) and not request.user.is_superuser:
            #     return ErrorResponse(msg="You cannot create global unit.")

            # 判断调整阀的item是否存在
            item = data.get("item", "")
            self.create_item_check(item)

            # 根据模式不同获取不同序列化器
            serializer = self.get_matching_serializer(int(mode), int(data.get("high_low", 0)))
            if serializer is None:
                return ErrorResponse(msg="The mode '%s' dose not exists" % mode)

            serializer = serializer(data=data, request=request)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            data = serializer.data
            data["label"] = "Valve"
            return DetailResponse(data=data, msg="新增成功")

        else:
            return ErrorResponse(msg="The 'mode' parameter must be passed.")

    def update(self, request, *args, **kwargs):
        data = request.data.copy()
        instance = self.get_object()
        data.pop("project", None)
        data.pop("mode", None)
        data.pop("is_global", None)

        # 不是超管不能修改全局部件
        # if instance.is_global and not request.user.is_superuser:
        #     return ErrorResponse(msg="You can't modify the global unit.")

        # 不能修改绑定的项目
        # if str(pid) != str(instance.project_id):
        #     return ErrorResponse(msg="You cannot modify the project bound to unit.")

        # 判断调整阀的item是否被占用
        item = data.get("item", "")
        self.update_item_check(instance.item, item)

        # 根据模式不同获取不同序列化器
        serializer = self.get_matching_serializer(instance.mode, int(data.get("high_low", 0)))
        serializer = serializer(instance=instance, data=data, request=request, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return DetailResponse(data=serializer.data, msg="编辑成功")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_matching_serializer(instance.mode, instance.high_low)
        serializer = serializer(instance, request=request)

        # 获取可显示的label
        labels = self.label_show()
        # 所有字段
        all_fields = set(ValveListSerializer.Meta.exclude) - {"is_deleted"}

        c = int(instance.mode)
        if c == 0:
            # RV
            m = list(all_fields - set(RVValveSerializer.Meta.exclude))
            m.sort()
        elif c == 1:
            # EDU
            m = {
                "disable": sorted(list(all_fields - set(EDUValveSerializer.Meta.exclude))) + ["high_low"],
                "enable": sorted(list(set(EDUValveSerializer.Meta.exclude) - set(EDUHLValveSerializer.Meta.exclude)))
            }
        else:
            return ErrorResponse(msg="The unit_class '%s' dose not exists" % c)

        data = {
            "data": serializer.data,
            "MSE": m,
            "BES2": [],
            "BES3": [],
            "fields": labels
        }
        nf = []
        for i in data['fields']:
            if data[i]:
                nf.append(i)
        data['fields'] = nf
        return DetailResponse(data=data, msg="获取成功")

    def search_list(self, request, *args, **kwargs):
        unit_name = request.query_params.get("unit_name", None)
        unit_class = request.query_params.get("unit_class", None)
        project_id = request.query_params.get("project_id", '')
        if unit_name is not None and unit_class is not None:
            # 获取可显示的label
            labels = self.label_show()
            # 所有字段
            all_fields = set(ValveListSerializer.Meta.exclude) - {"is_deleted"}

            c = int(unit_class)
            if c == 0:
                # RV
                b2 = list(all_fields - set(RVValveSerializer.Meta.exclude))
                b2.sort()
            elif c == 1:
                # EDU
                b2 = {
                    "disable": sorted(list(all_fields - set(EDUValveSerializer.Meta.exclude))) + ["high_low"],
                    "enable": sorted(list(set(EDUValveSerializer.Meta.exclude) - set(EDUHLValveSerializer.Meta.exclude)))
                }
            else:
                return ErrorResponse(msg="The unit_class '%s' dose not exists" % c)

            datas = []
            q = Q(item__icontains=unit_name, mode=unit_class)
            if project_id:
                q = q & Q(Q(project=project_id) | Q(is_global=True))
            else:
                q = q & Q(is_global=True)
            qs = Valve.objects.filter(q)[:self.LIMIT]
            for i in qs:
                serializer = self.get_matching_serializer(int(i.mode), int(i.high_low))(instance=i)
                data = {
                    "unit_name": i.item,
                    "data": serializer.data,
                    "MSE": [],
                    "BES2": b2,
                    "BES3": [],
                    "fields": labels
                }
                nf = []
                for j in data['fields']:
                    if data[j]:
                        nf.append(j)
                data['fields'] = nf
                datas.append(data)
            return SuccessResponse(data=datas, msg="获取成功", total=len(datas))

        else:
            return ErrorResponse(msg="The 'unit_name' and 'unit_class' parameter must be passed.")

    def create_fields(self, request, *args, **kwargs):
        # 新项目的新增时的需求字段返回
        mode = request.query_params.get("unit_class", "")
        if mode != "":
            # 获取可显示的label
            labels = self.label_show()
            # 所有字段
            all_fields = set(ValveListSerializer.Meta.exclude) - {"is_deleted", "high_low"}

            c = int(mode)
            if c == 0:
                # RV
                m = list(all_fields - set(RVValveSerializer.Meta.exclude))
                m.sort()
            elif c == 1:
                # EDU
                m = {
                    "disable": sorted(list(all_fields - set(EDUValveSerializer.Meta.exclude))) + ["high_low"],
                    "enable": sorted(list(set(EDUValveSerializer.Meta.exclude) - set(EDUHLValveSerializer.Meta.exclude)))
                }
            else:
                return ErrorResponse(msg="The unit_class '%s' dose not exists" % c)

        else:
            return ErrorResponse(msg="The 'unit_class' parameter must be passed.")

        fields = {
            "MSE": m,
            "BES2": [],
            "BES3": [],
            "fields": labels
        }
        nf = []
        for i in fields['fields']:
            if fields[i]:
                nf.append(i)
        fields['fields'] = nf
        return SuccessResponse(data=fields, msg="获取成功")
