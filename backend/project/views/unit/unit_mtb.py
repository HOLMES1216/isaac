from django.db.models import Q

from project.views.unit.unit import UnitCommonViewSet
from project.serializers.unit import MTBSerializer, MTBListSerializer
from project.models import MTB
from dvadmin.utils.json_response import DetailResponse, SuccessResponse, ErrorResponse


class MTBViewSet(UnitCommonViewSet):
    """
    调整阀增删改查接口
    """
    MODEL = MTB

    def get_matching_serializer(self):
        serializer = MTBSerializer
        print("mtb serializer is", serializer)
        return serializer

    def list(self, request, *args, **kwargs):
        query_param = request.query_params.get("mtb_type", "")
        search = request.query_params.get("search", None)  # 模糊搜索值
        if query_param != "":
            if (i := int(query_param)) in range(len(MTB.MTB_TYPE_CHOICES)):
                q = bq = Q(mtb_type=i)
                if not request.user.is_superuser:
                    q = Q(is_global=True) | Q(creator=request.user)
                    if pid := request.query_params.get("project", None):
                        q = q | Q(project=pid)
                    q = q & bq
                if search:
                    q = q & Q(item__icontains=search)
                queryset = MTB.objects.filter(q)[:self.LIMIT]
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = MTBListSerializer(page, many=True, request=request)
                    return self.get_paginated_response(serializer.data)
                serializer = MTBListSerializer(instance=queryset, many=True, request=request)
                return SuccessResponse(data=serializer.data, msg="获取成功", total=queryset.count())

            else:
                return ErrorResponse(msg="The mtb_type '%s' is not exists." % i)

        else:
            return ErrorResponse(msg="The 'mtb_type' parameter must be passed.")

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        # 如果project给了个''
        if data.get("project", "") == "":
            data.pop("project", None)
        data.pop("is_global", None)

        mtb_type = data.get("mtb_type", "")
        if mtb_type != "":
            # 不是超管不能创建全局部件
            # if int(data.get("is_global")) and not request.user.is_superuser:
            #     return ErrorResponse(msg="You cannot create global unit.")

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
            return DetailResponse(data=data, msg="新增成功")

        else:
            return ErrorResponse(msg="The 'mode' parameter must be passed.")

    def update(self, request, *args, **kwargs):
        data = request.data.copy()
        instance = self.get_object()
        data.pop("project", None)
        data.pop("is_global", None)
        data.pop("mtb_type", None)  # 不能修改类型

        # 不是超管不能修改全局部件
        # if instance.is_global and not request.user.is_superuser:
        #     return ErrorResponse(msg="You can't modify the global unit.")

        # 不能修改绑定的项目
        # if str(pid) != str(instance.project_id):
        #     return ErrorResponse(msg="You cannot modify the project bound to unit.")

        # 判断制动器item是否已被占用
        item = data.get("item", "")
        self.update_item_check(instance.item, item)

        serializer = self.get_matching_serializer()
        serializer = serializer(instance=instance, data=data, request=request, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return DetailResponse(data=serializer.data, msg="编辑成功")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_matching_serializer()
        serializer = serializer(instance, request=request)

        # 获取可显示的label
        labels = self.label_show()
        # 所有字段
        all_fields = set(MTBListSerializer.Meta.exclude) - {"is_deleted"}
        data = {
            "data": serializer.data,
            "MSE": sorted(list(all_fields)),
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
            if int(unit_class) not in range(len(MTB.MTB_TYPE_CHOICES)):
                return ErrorResponse(msg="The unit_class '%s' dose not exists" % unit_class)
            # 获取可显示的label
            labels = self.label_show()
            # 所有字段
            all_fields = set(MTBListSerializer.Meta.exclude) - {"is_deleted"}

            datas = []
            q = Q(item__icontains=unit_name, mtb_type=unit_class)
            if project_id:
                q = q & Q(Q(project=project_id) | Q(is_global=True))
            else:
                q = q & Q(is_global=True)
            qs = MTB.objects.filter(q)[:self.LIMIT]
            serializer = self.get_matching_serializer()
            for i in qs:
                serializer_instance = serializer(instance=i)
                data = {
                    "unit_name": i.item,
                    "data": serializer_instance.data,
                    "MSE": sorted(list(all_fields)),
                    "BES2": [],
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
        # 获取可显示的label
        labels = self.label_show()
        # 所有字段
        all_fields = set(MTBListSerializer.Meta.exclude) - {"is_deleted"}
        m = list(all_fields)
        m.sort()
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
