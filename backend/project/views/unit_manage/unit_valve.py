from project.models import Valve
from project.serializers.unit import (
    ValveListSerializer,
    ValveManagementListSerializer,
    RVValveSerializer,
    EDUValveSerializer,
    EDUHLValveSerializer
)
from project.views.unit_manage.unit import CommonViewSet, ValveFilter
from dvadmin.utils.json_response import ErrorResponse, DetailResponse, SuccessResponse


class ValveManagementViewSet(CommonViewSet):
    """
    调整阀管理的增删改查
    """
    filter_class = ValveFilter
    serializer_class = ValveManagementListSerializer
    MODEL = Valve
    UNIT_CLASS = 3

    def get_matching_serializer(self, mode, high_low):
        serializer = None
        if mode == 1:  # EDU
            if high_low:  # High/Low为True
                serializer = EDUHLValveSerializer
            else:  # High/Low为False
                serializer = EDUValveSerializer
        elif mode == 0:  # RV
            serializer = RVValveSerializer
        print("valve serializer is", serializer)
        return serializer

    def create(self, request, *args, **kwargs):
        self.permission_check("MSE")
        data = request.data.copy()
        # 如果project给了个''
        if data.get("project", "") == "":
            data.pop("project", None)
        data.pop("is_global", None)  # 部件管理里自动创建全局部件
        checker_id = data.pop("checker", None)
        if not checker_id:
            return ErrorResponse(msg="You must be choice a checker.")
        checker = self.get_checker(checker_id[0])

        mode = data.get("mode", "")
        if mode != "":
            data["is_global"] = True  # 默认全局部件

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
            self.create_check(serializer.instance, checker)
            return DetailResponse(data=data, msg="新增成功")

        else:
            return ErrorResponse(msg="The 'mode' parameter must be passed.")

    def update(self, request, *args, **kwargs):
        self.permission_check("MSE")
        data = request.data.copy()
        instance = self.get_object()
        data.pop("project", None)
        data.pop("mode", None)
        data.pop("is_global", None)
        checker_id = data.pop("checker", None)
        if not checker_id:
            return ErrorResponse(msg="You must be choice a checker.")
        checker = self.get_checker(checker_id)

        # 判断调整阀的item是否被占用
        item = data.get("item", "")
        self.update_item_check(instance.item, item)

        # 根据模式不同获取不同序列化器
        serializer = self.get_matching_serializer(instance.mode, int(data.get("high_low", 0)))
        serializer = serializer(instance=instance, data=data, request=request, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        self.create_check(instance, checker)
        return DetailResponse(data=serializer.data, msg="编辑成功")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_matching_serializer(instance.mode, instance.high_low)
        serializer = serializer(instance, request=request)

        # 所有字段
        all_fields = set(ValveListSerializer.Meta.exclude) - {"is_deleted"}

        c = int(instance.mode)
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

        data = {
            "data": serializer.data,
            "MSE": b2,
            "BES2": [],
            "BES3": [],
            "fields": ["MSE"]
        }
        return DetailResponse(data=data, msg="获取成功")

    def create_fields(self, request, *args, **kwargs):
        # 新项目的新增时的需求字段返回
        self.permission_check("MSE")
        mode = request.query_params.get("unit_class", "")
        if mode != "":
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
            "fields": ["MSE"]
        }
        return SuccessResponse(data=fields, msg="获取成功")
