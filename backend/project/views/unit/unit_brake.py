from django.db.models import Q

from project.views.unit.unit import UnitCommonViewSet
from project.serializers.unit import (
    BrakeTypeSerializer,
    BrakeListSerializer,
    RZWheelWZAxleBrakeAllSerializer,
    OtherWheelAxleBrakeAllSerializer,
    TreadBrakeAllSerializer,
    BrakePartSerializer,
    WheelAxleBrakeMSESerializer
)
from project.models import Brake, BrakeType
from dvadmin.utils.json_response import DetailResponse, SuccessResponse, ErrorResponse
from dvadmin.utils.viewset import CustomModelViewSet


class BrakeViewSet(UnitCommonViewSet):
    """
    制动器(轮装/轴装/踏面)增删改查接口
    """
    MODEL = Brake

    # swagger_fake_view = True
    
    def get_matching_serializer(self, type_of_brake, brake_type_name):
        serializer = None
        roles = self.request.user.role.values_list('name', flat=True)
        opt = ("RZ", "WZ")
        if self.request.user.is_superuser or "BES3" in roles:  # 超管和BES3，全部字段
            if type_of_brake in [0, 1]:  # 轮装/轴装
                if brake_type_name == opt[type_of_brake]:  # RZ/WZ类型
                    serializer = RZWheelWZAxleBrakeAllSerializer
                else:  # 其他类型
                    serializer = OtherWheelAxleBrakeAllSerializer
            elif type_of_brake == 2:  # 踏面
                serializer = TreadBrakeAllSerializer

        elif "BES2" in roles:  # BES2，轮装/轴装全部字段，踏面无字段
            if type_of_brake in [0, 1]:  # 轮装/轴装
                if brake_type_name == opt[type_of_brake]:  # RZ/WZ类型
                    serializer = RZWheelWZAxleBrakeAllSerializer
                else:  # 其他类型
                    serializer = OtherWheelAxleBrakeAllSerializer
            elif type_of_brake == 2:  # 踏面
                serializer = BrakePartSerializer

        elif "MSE" in roles:  # MSE，踏面全部字段，轮装/轴装部分字段
            if type_of_brake in [0, 1]:  # 轮装/轴装
                serializer = WheelAxleBrakeMSESerializer
            elif type_of_brake == 2:  # 踏面
                serializer = TreadBrakeAllSerializer

        else:
            serializer = BrakePartSerializer

        print("brake serializer is", serializer)
        return serializer

    def list(self, request, *args, **kwargs):
        query_param = request.query_params.get("type_of_brake", "")  # 指定的部件大类，0轮装 1轴装 2踏面
        search = request.query_params.get("search", "")  # 模糊搜索值
        search_type = request.query_params.get("search_type", None)  # 搜索的类型id，如RZ类型的类型id
        if query_param != "":
            if (i := int(query_param)) in range(len(BrakeType.BRAKE_TYPE_CHOICES)):
                q = bq = Q(brake_type__type_of_brake=i)
                if not request.user.is_superuser:
                    q = Q(is_global=True) | Q(creator=request.user)
                    if pid := request.query_params.get("project", None):
                        q = q | Q(project=pid)
                    q = q & bq
                if search:
                    q = q & Q(item__icontains=search)
                if search_type:
                    q = q & Q(brake_type=search_type)
                queryset = Brake.objects.filter(q)[:self.LIMIT]
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = BrakeListSerializer(page, many=True, request=request)
                    return self.get_paginated_response(serializer.data)
                serializer = BrakeListSerializer(instance=queryset, many=True, request=request)
                return SuccessResponse(data=serializer.data, msg="获取成功", total=queryset.count())

            else:
                return ErrorResponse(msg="The type_of_brake '%s' is not exists." % i)

        else:
            return ErrorResponse(msg="The 'type_of_brake' parameter must be passed.")

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        # 如果project给了个''
        if data.get("project", "") == "":
            data.pop("project", None)
        data.pop("is_global", None)  # 项目里没法创建全局部件

        type_of_brake = data.get("type_of_brake", "")
        if type_of_brake != "":
            # 不是超管不能创建全局部件
            # if int(data.get("is_global")) and not request.user.is_superuser:
            #     return ErrorResponse(msg="You cannot create global unit.")

            # 如果item值的结尾是'(*PB*)'，则bp_force值不能为0
            item = data.get("item", "")
            if item.endswith("(*PB*)") and float(data.get("pb_force", 0)) == 0:
                return ErrorResponse(msg="If the 'item' value ends in '(*PB*)', then 'bp_force' value cannot be '0'.")

            # 判断制动器item是否已存在
            self.create_item_check(item)

            # 判断指定的制动器类型是否存在
            brake_type = data.get("brake_type", "")
            brake_type_instance = BrakeType.objects.filter(pk=brake_type)
            if not brake_type_instance.exists():
                return ErrorResponse(msg="The brake_type '%s' is not exists." % brake_type)

            brake_type_name = brake_type_instance.first().name
            serializer = self.get_matching_serializer(int(type_of_brake), brake_type_name)
            if serializer is None:
                return ErrorResponse(msg="The type_of_brake '%s' is not exists." % type_of_brake)

            serializer = serializer(data=data, request=request)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            data = serializer.data
            data["label"] = "Brake"
            return DetailResponse(data=data, msg="新增成功")

        else:
            return ErrorResponse(msg="The 'type_of_brake' parameter must be passed.")

    def update(self, request, *args, **kwargs):
        data = request.data.copy()
        instance = self.get_object()
        type_of_brake = instance.brake_type.type_of_brake
        data.pop("project", None)
        data.pop("type_of_brake", None)
        data.pop("is_global", None)
        data.pop("brake_type", None)  # 不能修改类型

        # 项目里不能修改全局部件
        if instance.is_global:
            return ErrorResponse(msg="You can't modify the global unit.")

        # 不能修改绑定的项目
        # if str(pid) != str(instance.project_id):
        #     return ErrorResponse(msg="You cannot modify the project bound to unit.")

        # 如果item值的结尾是'(*PB*)'，则bp_force值不能为0
        item = data.get("item", "")
        if item.endswith("(*PB*)") and float(data.get("pb_force", 0)) == 0:
            return ErrorResponse(msg="If the 'item' value ends in '(*PB*)', then 'bp_force' value cannot be '0'.")

        # 判断指定的制动器类型是否存在
        # brake_type = data.get("brake_type", "")
        # brake_type_instance = BrakeType.objects.filter(pk=brake_type)
        # if not brake_type_instance.exists():
        #     return ErrorResponse(msg="The brake_type '%s' is not exists." % brake_type)

        # 判断制动器item是否已被占用
        self.update_item_check(instance.item, item)

        # brake_type_name = brake_type_instance.first().name
        brake_type_name = instance.brake_type.name
        serializer = self.get_matching_serializer(int(type_of_brake), brake_type_name)
        serializer = serializer(instance=instance, data=data, request=request, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return DetailResponse(data=serializer.data, msg="编辑成功")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        brake_type = instance.brake_type
        serializer = self.get_matching_serializer(int(brake_type.type_of_brake), brake_type.name)
        serializer = serializer(instance, request=request)

        # 获取可显示的label
        labels = self.label_show()
        # MSE可见部分的字段
        mse_fields = set(BrakeListSerializer.Meta.exclude) - set(TreadBrakeAllSerializer.Meta.exclude)
        # BES2可见部分的字段
        bes2_fields = set(BrakeListSerializer.Meta.exclude) - mse_fields
        # 找出序列化器里可见的部件字段
        unit_fields = set(BrakeListSerializer.Meta.exclude) & set(serializer.fields.keys())
        m = list(mse_fields & unit_fields)
        m.sort()
        b2 = list(bes2_fields & unit_fields)
        b2.sort()
        data = {
            "data": serializer.data,
            "MSE": m,
            "BES2": b2,
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
        unit_type = request.query_params.get("unit_type", None)
        project_id = request.query_params.get("project_id", None)
        if unit_name is not None and unit_class is not None:
            if int(unit_class) not in range(len(BrakeType.BRAKE_TYPE_CHOICES)):
                return ErrorResponse(msg="The unit_class '%s' dose not exists" % unit_class)

            # 获取可显示的label
            labels = self.label_show()
            # MSE可见部分的字段
            mse_fields = set(BrakeListSerializer.Meta.exclude) - set(TreadBrakeAllSerializer.Meta.exclude)
            # BES2可见部分的字段
            bes2_fields = set(BrakeListSerializer.Meta.exclude) - mse_fields - {"is_deleted"}

            datas = []
            q = Q(item__icontains=unit_name, brake_type__type_of_brake=unit_class)
            if unit_type:
                q = q & Q(brake_type=unit_type)
            if project_id:
                q = q & Q(Q(project=project_id) | Q(is_global=True))
            else:
                q = q & Q(is_global=True)
            qs = Brake.objects.filter(q)[:self.LIMIT]
            for i in qs:
                brake_type = i.brake_type
                serializer = self.get_matching_serializer(int(brake_type.type_of_brake), brake_type.name)(instance=i)
                # 找出序列化器里可见的部件字段
                unit_fields = set(BrakeListSerializer.Meta.exclude) & set(serializer.fields.keys())
                m = list(mse_fields & unit_fields)
                m.sort()
                b2 = list(bes2_fields & unit_fields)
                b2.sort()
                data = {
                    "unit_name": i.item,
                    "data": serializer.data,
                    "MSE": m,
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
        type_of_brake = request.query_params.get("unit_class", "")
        if type_of_brake != "":
            # 获取可显示的label
            labels = self.label_show()
            # MSE可见部分的字段
            mse_fields = set(BrakeListSerializer.Meta.exclude) - set(TreadBrakeAllSerializer.Meta.exclude)
            # BES2可见部分的字段
            bes2_fields = set(BrakeListSerializer.Meta.exclude) - mse_fields - {"is_deleted"}

            c = int(type_of_brake)
            if c == 0:
                # 轮装
                m = list(mse_fields - set(RZWheelWZAxleBrakeAllSerializer.Meta.exclude))
                rz_fields = list(bes2_fields & set(OtherWheelAxleBrakeAllSerializer.Meta.exclude))
                rz_fields.sort()
                other_fields = list(bes2_fields & set(RZWheelWZAxleBrakeAllSerializer.Meta.exclude))
                other_fields.sort()
                b2 = {
                    "RZ": rz_fields,
                    "Other": other_fields
                }
            elif c == 1:
                # 轴装
                m = list(mse_fields - set(RZWheelWZAxleBrakeAllSerializer.Meta.exclude))
                wz_fields = list(bes2_fields & set(OtherWheelAxleBrakeAllSerializer.Meta.exclude))
                wz_fields.sort()
                other_fields = list(bes2_fields & set(RZWheelWZAxleBrakeAllSerializer.Meta.exclude))
                other_fields.sort()
                b2 = {
                    "WZ": wz_fields,
                    "Other": other_fields
                }
            elif c == 2:
                # 踏面
                m = list(mse_fields)
                b2 = []
            else:
                return ErrorResponse(msg="The unit_class '%s' dose not exists" % c)

        else:
            return ErrorResponse(msg="The 'unit_class' parameter must be passed.")

        m.sort()
        fields = {
            "MSE": m,
            "BES2": b2,
            "BES3": [],
            "fields": labels
        }
        nf = []
        for i in fields['fields']:
            if fields[i]:
                nf.append(i)
        fields['fields'] = nf
        return SuccessResponse(data=fields, msg="获取成功")


class BrakeTypeViewSet(CustomModelViewSet):
    """
    制动器类型接口
    """
    filter_fields = ["type_of_brake"]
    queryset = BrakeType.objects.all()
    serializer_class = BrakeTypeSerializer
