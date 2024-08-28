from project.models import Brake, BrakeType
from project.serializers.unit import (
    BrakeListSerializer,
    OtherWheelAxleBrakeAllSerializer,
    TreadBrakeAllSerializer,
    RZWheelWZAxleBrakeAllSerializer,
    BrakeManagementListSerializer
)
from project.views.unit_manage.unit import CommonViewSet, BrakeFilter
from dvadmin.utils.json_response import ErrorResponse, DetailResponse, SuccessResponse


class BrakeManagementViewSet(CommonViewSet):
    """
    制动器管理的增删改查
    """
    filter_class = BrakeFilter
    serializer_class = BrakeManagementListSerializer
    MODEL = Brake
    UNIT_CLASS = 0  # Brake

    def get_matching_serializer(self, type_of_brake, brake_type_name):
        serializer = None
        opt = ("RZ", "WZ")
        if type_of_brake in [0, 1]:  # 轮装/轴装
            if brake_type_name == opt[type_of_brake]:  # RZ/WZ类型
                serializer = RZWheelWZAxleBrakeAllSerializer
            else:  # 其他类型
                serializer = OtherWheelAxleBrakeAllSerializer
        elif type_of_brake == 2:  # 踏面
            serializer = TreadBrakeAllSerializer
        print("brake serializer is", serializer)
        return serializer

    def create(self, request, *args, **kwargs):
        self.permission_check("BES2")
        data = request.data.copy()
        # data.pop("project", None)
        data.pop("is_global", None)  # 部件管理里自动创建全局部件
        # checker_id = data.pop("checker", None)
        # if not checker_id:
        #     return ErrorResponse(msg="You must be choice a checker.")
        # checker = self.get_checker(checker_id)

        type_of_brake = data.get("type_of_brake", "")
        if type_of_brake != "":
            data["is_global"] = True  # 默认全局部件

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
            # self.create_check(serializer.instance, checker)
            return DetailResponse(data=data, msg="新增成功")

        else:
            return ErrorResponse(msg="The 'type_of_brake' parameter must be passed.")

    def update(self, request, *args, **kwargs):
        self.permission_check("BES2")
        data = request.data.copy()
        instance = self.get_object()
        type_of_brake = instance.brake_type.type_of_brake
        # data.pop("project", None)
        data.pop("type_of_brake", None)
        data.pop("is_global", None)
        data.pop("brake_type", None)  # 不能修改类型
        # checker_id = data.pop("checker", None)
        # if not checker_id:
        #     return ErrorResponse(msg="You must be choice a checker.")
        # checker = self.get_checker(checker_id)

        # 如果item值的结尾是'(*PB*)'，则bp_force值不能为0
        item = data.get("item", "")
        if item.endswith("(*PB*)") and float(data.get("pb_force", 0)) == 0:
            return ErrorResponse(msg="If the 'item' value ends in '(*PB*)', then 'bp_force' value cannot be '0'.")

        # 判断制动器item是否已被占用
        self.update_item_check(instance.item, item)

        brake_type_name = instance.brake_type.name
        serializer = self.get_matching_serializer(int(type_of_brake), brake_type_name)
        serializer = serializer(instance=instance, data=data, request=request, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        # self.create_check(instance, checker)
        return DetailResponse(data=serializer.data, msg="编辑成功")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        brake_type = instance.brake_type
        serializer = self.get_matching_serializer(int(brake_type.type_of_brake), brake_type.name)
        serializer = serializer(instance, request=request)

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
            "fields": ["MSE", "BES2"]
        }
        return DetailResponse(data=data, msg="获取成功")

    def create_fields(self, request, *args, **kwargs):
        # 新项目的新增时的需求字段返回
        self.permission_check("BES2")
        type_of_brake = request.query_params.get("unit_class", "")
        if type_of_brake != "":
            # BES2可看所有字段
            fields = set(BrakeListSerializer.Meta.exclude)

            c = int(type_of_brake)
            if c == 0:
                # 轮装
                rz_fields = list(fields - set(RZWheelWZAxleBrakeAllSerializer.Meta.exclude))
                rz_fields.sort()
                other_fields = list(fields - set(OtherWheelAxleBrakeAllSerializer.Meta.exclude))
                other_fields.sort()
                b2 = {
                    "RZ": rz_fields,  # rz类型轮装
                    "Other": other_fields  # 其他类型轮装
                }
            elif c == 1:
                # 轴装
                wz_fields = list(fields - set(RZWheelWZAxleBrakeAllSerializer.Meta.exclude))
                wz_fields.sort()
                other_fields = list(fields - set(OtherWheelAxleBrakeAllSerializer.Meta.exclude))
                other_fields.sort()
                b2 = {
                    "WZ": wz_fields,  # wz类型轮装
                    "Other": other_fields  # 其他类型轮装
                }
            elif c == 2:
                # 踏面
                b2 = list(fields - set(TreadBrakeAllSerializer.Meta.exclude))
                b2.sort()
            else:
                return ErrorResponse(msg="The unit_class '%s' dose not exists" % c)

        else:
            return ErrorResponse(msg="The 'unit_class' parameter must be passed.")

        fields = {
            "MSE": [],
            "BES2": b2,
            "BES3": [],
            "fields": ["BES2"]
        }
        return SuccessResponse(data=fields, msg="获取成功")
