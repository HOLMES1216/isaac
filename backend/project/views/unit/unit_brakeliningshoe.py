from django.db.models import Q

from project.views.unit.unit import UnitCommonViewSet
from project.serializers.unit import (
    PadTypeListSerializer,
    BrakeLiningShoeListSerializer,
    BrakeLiningAllSerializer,
    BrakeShoeAllSerializer,
    BrakeLiningShoePartSerializer
)
from project.models import BrakeLiningShoe, PadType
from dvadmin.utils.json_response import DetailResponse, SuccessResponse, ErrorResponse
from dvadmin.utils.viewset import CustomModelViewSet


class PadViewSet(UnitCommonViewSet):
    """
    闸片/闸瓦类型增删改查接口
    """
    MODEL = BrakeLiningShoe
    
    # swagger_fake_view = True

    def get_matching_serializer(self, type_of_pad):
        serializer = None
        if self.request.user.is_superuser:  # 超管，全部字段
            if type_of_pad == 0:  # 闸片
                serializer = BrakeLiningAllSerializer
            elif type_of_pad == 1:  # 闸瓦
                serializer = BrakeShoeAllSerializer

        elif "BES2" in self.request.user.role.values_list('name', flat=True):  # BES2，全部字段
            if type_of_pad == 0:  # 闸片
                serializer = BrakeLiningAllSerializer
            elif type_of_pad == 1:  # 闸瓦
                serializer = BrakeShoeAllSerializer

        else:
            serializer = BrakeLiningShoePartSerializer

        print("brake lining / brake shoe serializer is", serializer)
        return serializer

    def list(self, request, *args, **kwargs):
        query_param = request.query_params.get("type_of_pad", "")
        search = request.query_params.get("search", "")  # 模糊搜索值
        search_type = request.query_params.get("search_type", "")  # 搜索的类型id
        if query_param != "":
            if (i := int(query_param)) in range(len(BrakeLiningShoe.PAD_TYPE_CHOICES)):
                q = bq = Q(type_of_pad=i)
                if not request.user.is_superuser:
                    q = Q(is_global=True) | Q(creator=request.user)
                    if pid := request.query_params.get("project", None):
                        q = q | Q(project=pid)
                    q = q & bq
                if search:
                    q = q & Q(item__icontains=search)
                if search_type:
                    q = q & Q(pad_type=search_type)
                queryset = BrakeLiningShoe.objects.filter(q)[:self.LIMIT]
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = BrakeLiningShoeListSerializer(page, many=True, request=request)
                    return self.get_paginated_response(serializer.data)
                serializer = BrakeLiningShoeListSerializer(instance=queryset, many=True, request=request)
                return SuccessResponse(data=serializer.data, msg="获取成功", total=queryset.count())

            else:
                return ErrorResponse(msg="The type_of_pad '%s' dose not exists" % i)

        else:
            return ErrorResponse(msg="The 'type_of_pad' parameter must be passed")

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        # 如果project给了个''
        if data.get("project", "") == "":
            data.pop("project", None)
        data.pop("is_global", None)  # 项目里没法创建全局部件

        type_of_pad = data.get("type_of_pad", "")
        if type_of_pad != "":
            # 不是超管不能创建全局部件
            # if int(data.get("is_global")) and not request.user.is_superuser:
            #     return ErrorResponse(msg="You cannot create global unit.")

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
        data = request.data.copy()
        instance = self.get_object()
        type_of_pad = instance.type_of_pad
        data.pop("project", None)
        data.pop("type_of_pad", None)
        data.pop("is_global", None)
        data.pop("pad_type", None)  # 不能修改类型

        # 不是超管不能修改全局部件
        if instance.is_global and not request.user.is_superuser:
            return ErrorResponse(msg="You can't modify the global unit.")

        # 不能修改绑定的项目
        # if str(pid) != str(instance.project_id):
        #     return ErrorResponse(msg="You cannot modify the project bound to unit.")

        # 判断指定的材料类型是否存在
        # pad_type = data.get("pad_type", "")
        # pad_type_instance = PadType.objects.filter(pk=pad_type)
        # if not pad_type_instance.exists():
        #     return ErrorResponse(msg="The pad_type '%s' is not exists." % pad_type)

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

        # 获取可显示的label
        labels = self.label_show()
        # BES2可见部分的字段
        bes2_fields = set(BrakeLiningShoeListSerializer.Meta.exclude) - {"is_deleted"}
        # 找出序列化器里可见的部件字段
        unit_fields = set(BrakeLiningShoeListSerializer.Meta.exclude) & set(serializer.fields.keys())
        b2 = list(bes2_fields & unit_fields)
        b2.sort()
        data = {
            "data": serializer.data,
            "MSE": [],
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
            if int(unit_class) not in range(len(BrakeLiningShoe.PAD_TYPE_CHOICES)):
                return ErrorResponse(msg="The unit_class '%s' dose not exists" % unit_class)

            # 获取可显示的label
            labels = self.label_show()
            # BES2可见部分的字段
            bes2_fields = set(BrakeLiningShoeListSerializer.Meta.exclude) - {"is_deleted"}

            datas = []
            q = Q(item__icontains=unit_name, type_of_pad=unit_class)
            if unit_type:
                q = q & Q(pad_type=unit_type)
            if project_id:
                q = q & Q(Q(project=project_id) | Q(is_global=True))
            else:
                q = q & Q(is_global=True)
            qs = BrakeLiningShoe.objects.filter(q)[:self.LIMIT]
            serializer = self.get_matching_serializer(int(unit_class))
            for i in qs:
                serializer_instance = serializer(instance=i)
                unit_fields = set(BrakeLiningShoeListSerializer.Meta.exclude) & set(serializer_instance.fields.keys())
                b2 = list(bes2_fields & unit_fields)
                b2.sort()
                data = {
                    "unit_name": i.item,
                    "data": serializer_instance.data,
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
        type_of_pad = request.query_params.get("unit_class", "")
        if type_of_pad != "":
            # 获取可显示的label
            labels = self.label_show()

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


class PadTypeViewSet(CustomModelViewSet):
    """
    闸片/闸瓦材料类型接口
    """
    queryset = PadType.objects.all()
    serializer_class = PadTypeListSerializer
