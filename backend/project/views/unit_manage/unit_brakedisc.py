from project.models import BrakeDisc, BrakeDiscType
from project.serializers.unit import (
    BrakeDiscListSerializer,
    WheelBrakeDiscAllSerializer,
    AxleBrakeDiscAllSerializer,
    BrakeDiscManagementListSerializer
)
from project.views.unit_manage.unit import CommonViewSet, BrakeDiscFilter
from dvadmin.utils.json_response import ErrorResponse, DetailResponse, SuccessResponse


class BrakeDiscManagementViewSet(CommonViewSet):
    """
    制动盘管理的增删改查
    """
    filter_class = BrakeDiscFilter
    serializer_class = BrakeDiscManagementListSerializer
    MODEL = BrakeDisc
    UNIT_CLASS = 1

    def get_matching_serializer(self, type_of_disc):
        serializer = None
        if type_of_disc == 0:  # 轮装
            serializer = WheelBrakeDiscAllSerializer
        elif type_of_disc == 1:  # 轴装
            serializer = AxleBrakeDiscAllSerializer
        print("brakedisc serializer is", serializer)
        return serializer

    def create(self, request, *args, **kwargs):
        self.permission_check("BES3")
        data = request.data.copy()
        # data.pop("project", None)
        data.pop("is_global", None)  # 部件管理里自动创建全局部件
        data.pop("checker", None)

        type_of_disc = data.get("type_of_disc", "")
        if type_of_disc != "":
            data["is_global"] = True  # 默认全局部件

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
        self.permission_check("BES3")
        data = request.data.copy()
        instance = self.get_object()
        type_of_disc = instance.type_of_disc
        data.pop("project", None)
        data.pop("type_of_disc", None)
        data.pop("is_global", None)
        data.pop("disc_type", None)  # 不能修改类型
        data.pop("checker", None)

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
        self.permission_check("BES3")
        instance = self.get_object()
        serializer = self.get_matching_serializer(int(instance.type_of_disc))
        serializer = serializer(instance, request=request)

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
            "fields": ["BES3"]
        }
        return DetailResponse(data=data, msg="获取成功")

    def create_fields(self, request, *args, **kwargs):
        # 新项目的新增时的需求字段返回
        self.permission_check("BES3")
        type_of_disc = request.query_params.get("unit_class", "")
        if type_of_disc != "":
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
            "fields": ["BES3"]
        }
        return SuccessResponse(data=fields, msg="获取成功")
