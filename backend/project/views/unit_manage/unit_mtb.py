from project.models import MTB
from project.serializers.unit import MTBListSerializer, MTBSerializer, MTBManagementListSerializer
from project.views.unit_manage.unit import CommonViewSet, MTBFilter
from dvadmin.utils.json_response import ErrorResponse, DetailResponse, SuccessResponse


class MTBManagementViewSet(CommonViewSet):
    """
    MTB磁轨制动器管理的增删改查
    """
    filter_class = MTBFilter
    serializer_class = MTBManagementListSerializer
    MODEL = MTB
    UNIT_CLASS = 4

    def get_matching_serializer(self):
        serializer = MTBSerializer
        print("mtb serializer is", serializer)
        return serializer

    def create(self, request, *args, **kwargs):
        self.permission_check("BES2")
        data = request.data.copy()
        # 如果project给了个''
        if data.get("project", "") == "":
            data.pop("project", None)
        data.pop("is_global", None)  # 部件管理里自动创建全局部件
        checker_id = data.pop("checker", None)
        if not checker_id:
            return ErrorResponse(msg="You must be choice a checker.")
        checker = self.get_checker(checker_id)

        mtb_type = data.get("mtb_type", "")
        if mtb_type != "":
            data["is_global"] = True  # 默认全局部件

            # 判断MTB的item是否存在
            item = data.get("item", "")
            self.create_item_check(item)

            if int(mtb_type) in range(len(MTB.MTB_TYPE_CHOICES)):
                serializer = MTBSerializer
            else:
                return ErrorResponse(msg="The mtb_type '%s' dose not exists" % mtb_type)

            serializer = serializer(data=data, request=request)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            data = serializer.data
            data["label"] = "MTB"
            self.create_check(serializer.instance, checker)
            return DetailResponse(data=data, msg="新增成功")

        else:
            return ErrorResponse(msg="The 'mode' parameter must be passed.")

    def update(self, request, *args, **kwargs):
        self.permission_check("BES2")
        data = request.data.copy()
        instance = self.get_object()
        data.pop("project", None)
        data.pop("is_global", None)
        data.pop("mtb_type", None)  # 不能修改类型
        checker_id = data.pop("checker", None)
        if not checker_id:
            return ErrorResponse(msg="You must be choice a checker.")
        checker = self.get_checker(checker_id)

        # 判断制动器item是否已被占用
        item = data.get("item", "")
        self.update_item_check(instance.item, item)

        serializer = self.get_matching_serializer()
        serializer = serializer(instance=instance, data=data, request=request, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        self.create_check(instance, checker)
        return DetailResponse(data=serializer.data, msg="编辑成功")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_matching_serializer()
        serializer = serializer(instance, request=request)
        # 所有字段
        all_fields = set(MTBListSerializer.Meta.exclude) - {"is_deleted"}
        data = {
            "data": serializer.data,
            "MSE": sorted(list(all_fields)),
            "BES2": [],
            "BES3": [],
            "fields": ["MSE"]
        }
        return DetailResponse(data=data, msg="获取成功")

    def create_fields(self, request, *args, **kwargs):
        # 新项目的新增时的需求字段返回
        self.permission_check("BES2")
        # 所有字段
        all_fields = set(MTBListSerializer.Meta.exclude) - {"is_deleted"}
        m = list(all_fields)
        m.sort()
        fields = {
            "MSE": m,
            "BES2": [],
            "BES3": [],
            "fields": ["MSE"]
        }
        return SuccessResponse(data=fields, msg="获取成功")
