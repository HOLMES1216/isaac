from project.models import BrakeLiningShoe, PadType
from project.serializers.unit import (
    BrakeLiningShoeListSerializer,
    BrakeShoeAllSerializer,
    BrakeLiningAllSerializer,
    BrakePadManagementListSerializer
)
from project.views.unit_manage.unit import CommonViewSet, BrakePadFilter
from dvadmin.utils.json_response import ErrorResponse, DetailResponse, SuccessResponse


class BrakeLiningShoeManagementViewSet(CommonViewSet):
    """
    闸片闸瓦管理的增删改查
    """
    filter_class = BrakePadFilter
    serializer_class = BrakePadManagementListSerializer
    MODEL = BrakeLiningShoe
    UNIT_CLASS = 2

    def get_matching_serializer(self, type_of_pad):
        serializer = None
        if type_of_pad == 0:  # 闸片
            serializer = BrakeLiningAllSerializer
        elif type_of_pad == 1:  # 闸瓦
            serializer = BrakeShoeAllSerializer
        print("brake lining / brake shoe serializer is", serializer)
        return serializer

    def create(self, request, *args, **kwargs):
        self.permission_check("BES3")
        data = request.data.copy()
        # 如果project给了个''
        if data.get("project", "") == "":
            data.pop("project", None)
        data.pop("is_global", None)  # 部件管理里自动创建全局部件
        data.pop("checker", None)

        type_of_pad = data.get("type_of_pad", "")
        if type_of_pad != "":
            data["is_global"] = True  # 默认全局部件

            # 判断指定的材料类型是否存在
            pad_type = data.get("pad_type", "")
            pad_type_instance = PadType.objects.filter(pk=pad_type)
            if not pad_type_instance.exists():
                return ErrorResponse(msg="The pad_type '%s' is not exists." % pad_type)

            # 判断闸片闸瓦item是否已存在
            item = data.get("item", "")
            self.create_item_check(item)

            # 根据类型不同获取不同序列化器
            serializer = self.get_matching_serializer(int(type_of_pad))
            if serializer is None:
                return ErrorResponse(msg="The type_of_pad '%s' dose not exists" % type_of_pad)

            serializer = serializer(data=data, request=request)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            data = serializer.data
            data["label"] = "Brake Pad"
            return DetailResponse(data=data, msg="新增成功")

        else:
            return ErrorResponse(msg="The 'type_of_pad' parameter must be passed.")

    def update(self, request, *args, **kwargs):
        self.permission_check("BES3")
        data = request.data.copy()
        instance = self.get_object()
        type_of_pad = instance.type_of_pad
        data.pop("project", None)
        data.pop("type_of_pad", None)
        data.pop("is_global", None)
        data.pop("pad_type", None)  # 不能修改类型
        data.pop("checker", None)

        # 判断制动器item是否已被占用
        item = data.get("item", "")
        self.update_item_check(instance.item, item)

        # 根据类型不同获取不同序列化器
        serializer = self.get_matching_serializer(int(type_of_pad))
        serializer = serializer(instance=instance, data=data, request=request, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return DetailResponse(data=serializer.data, msg="编辑成功")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_matching_serializer(int(instance.type_of_pad))
        serializer = serializer(instance, request=request)

        # BES2可见部分的字段
        bes2_fields = set(BrakeLiningShoeListSerializer.Meta.exclude) - {"is_deleted"}
        # 找出序列化器里可见的部件字段
        unit_fields = set(BrakeLiningShoeListSerializer.Meta.exclude) & set(serializer.fields.keys())
        b2 = list(bes2_fields & unit_fields)
        b2.sort()
        data = {
            "data": serializer.data,
            "MSE": [],
            "BES2": [],
            "BES3": b2,
            "fields": ["BES3"]
        }
        return DetailResponse(data=data, msg="获取成功")

    def create_fields(self, request, *args, **kwargs):
        # 新项目的新增时的需求字段返回
        self.permission_check("BES3")
        type_of_pad = request.query_params.get("unit_class", "")
        if type_of_pad != "":
            c = int(type_of_pad)
            if c == 0:
                # 闸片
                b2 = list(set(BrakeShoeAllSerializer.Meta.exclude) - {"is_deleted"})
            elif c == 1:
                # 闸瓦
                b2 = list(set(BrakeLiningAllSerializer.Meta.exclude) - {"is_deleted"})
            else:
                return ErrorResponse(msg="The unit_class '%s' dose not exists" % c)

        else:
            return ErrorResponse(msg="The 'unit_class' parameter must be passed.")

        b2.sort()
        fields = {
            "MSE": [],
            "BES2": [],
            "BES3": b2,
            "fields": ["BES3"]
        }
        return SuccessResponse(data=fields, msg="获取成功")
