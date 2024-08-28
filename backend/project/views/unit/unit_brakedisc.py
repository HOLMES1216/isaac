from django.db.models import Q

from project.views.unit.unit import UnitCommonViewSet
from project.serializers.unit import (
    BrakeDiscTypeListSerializer,
    BrakeDiscListSerializer,
    WheelBrakeDiscAllSerializer,
    AxleBrakeDiscAllSerializer,
    BrakeDiscPartSerializer
)
from project.models import BrakeDisc, BrakeDiscType
from dvadmin.utils.json_response import DetailResponse, SuccessResponse, ErrorResponse
from dvadmin.utils.viewset import CustomModelViewSet


class BrakeDiscViewSet(UnitCommonViewSet):
    """
    制动盘(轮装/轴装)增删改查接口
    """
    MODEL = BrakeDisc
    
    # swagger_fake_view = True

    def get_matching_serializer(self, type_of_disc):
        serializer = None
        roles = self.request.user.role.values_list('name', flat=True)
        if self.request.user.is_superuser or "BES3" in roles:  # 超管和BES3，全部字段
            if type_of_disc == 0:  # 轮装
                serializer = WheelBrakeDiscAllSerializer
            elif type_of_disc == 1:  # 轴装
                serializer = AxleBrakeDiscAllSerializer

        else:
            serializer = BrakeDiscPartSerializer

        print("brake disc serializer is", serializer)
        return serializer

    def list(self, request, *args, **kwargs):
        query_param = request.query_params.get("type_of_disc", "")
        search = request.query_params.get("search", "")  # 模糊搜索值
        search_type = request.query_params.get("search_type", None)  # 搜索的类型id
        if query_param != "":
            if (i := int(query_param)) in range(len(BrakeDisc.DISC_TYPE_CHOICES)):
                q = bq = Q(type_of_disc=i)
                if not request.user.is_superuser:
                    q = Q(is_global=True) | Q(creator=request.user)
                    if pid := request.query_params.get("project", None):
                        q = q | Q(project=pid)
                    q = q & bq
                if search:
                    q = q & Q(item__icontains=search)
                if search_type:
                    q = q & Q(disc_type=search_type)
                queryset = BrakeDisc.objects.filter(q)[:self.LIMIT]
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = BrakeDiscListSerializer(page, many=True, request=request)
                    return self.get_paginated_response(serializer.data)
                serializer = BrakeDiscListSerializer(instance=queryset, many=True, request=request)
                return SuccessResponse(data=serializer.data, msg="获取成功", total=queryset.count())

            else:
                return ErrorResponse(msg="The type_of_disc '%s' dose not exists" % i)

        else:
            return ErrorResponse(msg="The 'type_of_disc' parameter must Be passed")

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        # 如果project给了个''
        if data.get("project", "") == "":
            data.pop("project", None)
        data.pop("is_global", None)  # 项目里没法创建全局部件

        type_of_disc = data.get("type_of_disc", "")
        if type_of_disc != "":
            # 不是超管不能创建全局部件
            # if int(data.get("is_global")) and not request.user.is_superuser:
            #     return ErrorResponse(msg="You cannot create global unit.")

            # 判断指定的制动器材料类型是否存在
            disc_type = data.get("disc_type", "")
            disc_type_instance = BrakeDiscType.objects.filter(pk=disc_type)
            if not disc_type_instance.exists():
                return ErrorResponse(msg="The brake_type '%s' is not exists." % disc_type)

            # 判断制动盘item是否已存在
            item = data.get("item", "")
            self.create_item_check(item)

            # 根据类型不同获取不同序列化器
            serializer = self.get_matching_serializer(int(type_of_disc))
            if serializer is None:
                return ErrorResponse(msg="The type_of_disc '%s' dose not exists" % type_of_disc)

            serializer = serializer(data=data, request=request)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            data = serializer.data
            data["label"] = "Brake Disc"
            return DetailResponse(data=data, msg="新增成功")

        else:
            return ErrorResponse(msg="The 'type_of_disc' parameter must be passed.")

    def update(self, request, *args, **kwargs):
        data = request.data.copy()
        instance = self.get_object()
        type_of_disc = instance.type_of_disc
        data.pop("project", None)
        data.pop("type_of_disc", None)
        data.pop("is_global", None)
        data.pop("disc_type", None)  # 不能修改类型

        # 项目里不能修改全局部件
        if instance.is_global:
            return ErrorResponse(msg="You can't modify the global unit.")

        # 不能修改绑定的项目
        # if str(pid) != str(instance.project_id):
        #     return ErrorResponse(msg="You cannot modify the project bound to unit.")

        # 判断指定的制动器材料类型是否存在
        # disc_type = data.get("disc_type", "")
        # disc_type_instance = BrakeDiscType.objects.filter(pk=disc_type)
        # if not disc_type_instance.exists():
        #     return ErrorResponse(msg="The brake_type '%s' is not exists." % disc_type)

        # 判断制动器item是否已被占用
        item = data.get("item", "")
        self.update_item_check(instance.item, item)

        # 根据类型不同获取不同序列化器
        serializer = self.get_matching_serializer(int(type_of_disc))
        serializer = serializer(instance=instance, data=data, request=request, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return DetailResponse(data=serializer.data, msg="编辑成功")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_matching_serializer(int(instance.type_of_disc))
        serializer = serializer(instance, request=request)

        # 获取可显示的label
        labels = self.label_show()
        # BES3可见部分的字段
        bes3_fields = set(BrakeDiscListSerializer.Meta.exclude) - {"is_deleted"}
        # 找出序列化器里可见的部件字段
        unit_fields = set(BrakeDiscListSerializer.Meta.exclude) & set(serializer.fields.keys())
        b3 = list(bes3_fields & unit_fields)
        b3.sort()
        data = {
            "data": serializer.data,
            "MSE": [],
            "BES2": [],
            "BES3": b3,
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
        unit_type = request.query_params.get("unit_type", None)
        project_id = request.query_params.get("project_id", None)
        if unit_name is not None and unit_class is not None:
            if int(unit_class) not in range(len(BrakeDisc.DISC_TYPE_CHOICES)):
                return ErrorResponse(msg="The unit_class '%s' dose not exists" % unit_class)

            # 获取可显示的label
            labels = self.label_show()
            # BES3可见部分的字段
            bes3_fields = set(BrakeDiscListSerializer.Meta.exclude) - {"is_deleted"}

            datas = []
            q = Q(item__icontains=unit_name, type_of_disc=unit_class)
            if unit_type:
                q = q & Q(disc_type=unit_type)
            if project_id:
                q = q & Q(Q(project=project_id) | Q(is_global=True))
            else:
                q = q & Q(is_global=True)
            qs = BrakeDisc.objects.filter(q)[:self.LIMIT]
            serializer = self.get_matching_serializer(int(unit_class))
            for i in qs:
                serializer_instance = serializer(instance=i)
                # 找出序列化器里可见的部件字段
                unit_fields = set(BrakeDiscListSerializer.Meta.exclude) & set(serializer_instance.fields.keys())
                b3 = list(bes3_fields & unit_fields)
                b3.sort()
                data = {
                    "unit_name": i.item,
                    "data": serializer_instance.data,
                    "MSE": [],
                    "BES2": [],
                    "BES3": b3,
                    "fields": labels
                }
                nf = []
                for i in data['fields']:
                    if data[i]:
                        nf.append(i)
                data['fields'] = nf
                datas.append(data)
            return SuccessResponse(data=datas, msg="获取成功", total=len(datas))

        else:
            return ErrorResponse(msg="The 'unit_name' and 'unit_class' parameter must be passed.")

    def create_fields(self, request, *args, **kwargs):
        # 新项目的新增时的需求字段返回
        type_of_disc = request.query_params.get("unit_class", "")
        if type_of_disc != "":
            # 获取可显示的label
            labels = self.label_show()
            # BES3可见部分的字段
            bes3_fields = set(BrakeDiscListSerializer.Meta.exclude) - {"is_deleted"}

            c = int(type_of_disc)
            if c == 0:
                # 轮装
                b3 = list(bes3_fields - {"screw_envelope_outer_diameter"})
            elif c == 1:
                # 轴装
                b3 = list(bes3_fields)
            else:
                return ErrorResponse(msg="The unit_class '%s' dose not exists" % c)

        else:
            return ErrorResponse(msg="The 'unit_class' parameter must be passed.")

        b3.sort()
        fields = {
            "MSE": [],
            "BES2": [],
            "BES3": b3,
            "fields": labels
        }
        nf = []
        for i in fields['fields']:
            if fields[i]:
                nf.append(i)
        fields['fields'] = nf
        return SuccessResponse(data=fields, msg="获取成功")


class BrakeDiscTypeViewSet(CustomModelViewSet):
    """
    制动器材料类型接口
    """
    queryset = BrakeDiscType.objects.all()
    serializer_class = BrakeDiscTypeListSerializer
