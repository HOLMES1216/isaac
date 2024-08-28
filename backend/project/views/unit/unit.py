from django.db.models import Q
from rest_framework.exceptions import APIException

from project.serializers.unit import (
    BasicElementSerializer,
    CarSerializer,
    BrakeListSerializer,
    BrakeDiscListSerializer,
    BrakeLiningShoeListSerializer,
    ValveListSerializer,
    MTBListSerializer,
    BrakeDiscTypeListSerializer,
    BrakeTypeSerializer,
    PadTypeListSerializer
)
from dvadmin.utils.json_response import SuccessResponse, ErrorResponse, DetailResponse
from project.models import (
    BasicElement,
    Car,
    Brake,
    BrakeDisc,
    BrakeLiningShoe,
    Valve,
    MTB,
    BrakeType,
    BrakeDiscType,
    PadType
)
from dvadmin.utils.viewset import CustomModelViewSet


# 视图集
class UnitCommonViewSet(CustomModelViewSet):
    """
    所有部件一些公共的函数
    """
    MODEL = None
    LIMIT = 10

    def get_object(self):
        if self.MODEL is None:
            raise Exception("Please override the 'MODEL' property")
        queryset = self.MODEL.objects.filter(**self.kwargs)
        if not queryset.exists():
            raise APIException("Data is not exists.")
        return queryset.first()

    def destroy(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            return ErrorResponse(msg="You can't delete this product.")
        instance = self.get_object()
        if instance.is_global:
            return ErrorResponse(msg="You cannot delete global unit.")
        instance.delete()
        return DetailResponse(data=[], msg="删除成功")

    def create_item_check(self, item):
        """新增的时候判断item是否被占用"""
        if self.MODEL.objects.filter(item=item).exists():
            raise APIException("The item '%s' is exists." % item)

    def update_item_check(self, old_item, new_item):
        """编辑的时候判断item是否被占用"""
        if new_item != old_item and self.MODEL.objects.filter(item=new_item).exists():
            raise APIException("The item '%s' is exists." % new_item)

    def label_show(self):
        # 根据不同用户角色控制前端能看的标签页
        role_label = {
            "OTHER": [],
            "MSE": ["MSE"],
            "BES2": ["MSE", "BES2"],
            "BES3": ["MSE", "BES2", "BES3"]
        }
        if self.request.user.is_superuser:
            labels = role_label["BES3"]
        else:
            roles = self.request.user.role.values_list("name", flat=True)
            for i in ["BES3", "BES2", "MSE"]:
                if i in roles:
                    labels = role_label[i]
                    break
            else:
                labels = role_label["OTHER"]
        return labels


class AllUnitViewSet(CustomModelViewSet):
    """
    所有部件列表（固定头几条数据）接口
    """
    limit = 10

    def list(self, request, *args, **kwargs):
        all_data = {}
        q = Q()
        if not request.user.is_superuser:
            q = Q(is_global=True)
            if pid := request.query_params.get("project", None):
                q = q | Q(project=pid)

        # 基础部件
        queryset = BasicElement.objects.all()
        all_data[BasicElementSerializer.Meta.model._meta.model_name] = {
            "total": queryset.count(),
            "data": BasicElementSerializer(instance=queryset, many=True, request=request).data
        }

        # 车辆
        queryset = Car.objects.all()
        type_data = dict()
        for num, desc in Car.CAR_TYPE_CHOICES:
            type_queryset = queryset.filter(car_type=num)[:self.limit]
            type_data[desc] = CarSerializer(instance=type_queryset, many=True, request=request).data
        all_data[CarSerializer.Meta.model._meta.model_name] = {
            "total": queryset.count(),
            "data": type_data
        }

        # 制动器
        queryset = Brake.objects.filter(q)
        first = BrakeType.BRAKE_TYPE_CHOICES[0]
        type_queryset = queryset.filter(brake_type__type_of_brake=first[0])[:self.limit]
        all_data[BrakeListSerializer.Meta.model._meta.model_name] = {
            "total": queryset.count(),
            "data": BrakeListSerializer(instance=type_queryset, many=True, request=request).data
        }

        # 制动盘
        queryset = BrakeDisc.objects.filter(q)
        first = BrakeDisc.DISC_TYPE_CHOICES[0]
        type_queryset = queryset.filter(type_of_disc=first[0])[:self.limit]
        all_data[BrakeDiscListSerializer.Meta.model._meta.model_name] = {
            "total": queryset.count(),
            "data": BrakeDiscListSerializer(instance=type_queryset[:self.limit], many=True, request=request).data
        }

        # 闸片闸瓦
        queryset = BrakeLiningShoe.objects.filter(q)
        first = BrakeLiningShoe.PAD_TYPE_CHOICES[0]
        type_queryset = queryset.filter(type_of_pad=first[0])[:self.limit]
        all_data[BrakeLiningShoeListSerializer.Meta.model._meta.model_name] = {
            "total": queryset.count(),
            "data": BrakeLiningShoeListSerializer(instance=type_queryset, many=True, request=request).data
        }

        # 调整阀
        queryset = Valve.objects.filter(q)
        first = Valve.MODE[0]
        type_queryset = queryset.filter(mode=first[0])[:self.limit]
        all_data[ValveListSerializer.Meta.model._meta.model_name] = {
            "total": queryset.count(),
            "data": ValveListSerializer(instance=type_queryset, many=True, request=request).data
        }

        # MTB
        queryset = MTB.objects.filter(q)
        first = MTB.MTB_TYPE_CHOICES[0]
        type_queryset = queryset.filter(mtb_type=first[0])[:self.limit]
        all_data[MTBListSerializer.Meta.model._meta.model_name] = {
            "total": queryset.count(),
            "data": MTBListSerializer(instance=type_queryset, many=True, request=request).data
        }

        return SuccessResponse(data=all_data, msg="获取成功")


class AllUnitTypeViewSet(CustomModelViewSet):
    """
    所有有类型区分的部件列表接口
    """

    def list(self, request, *args, **kwargs):
        all_data = {}

        # 制动器
        data = []
        for ind, item in BrakeType.BRAKE_TYPE_CHOICES:
            queryset = BrakeType.objects.filter(type_of_brake=ind)
            data.append({
                "label": item,
                "total": queryset.count(),
                "data": BrakeTypeSerializer(instance=queryset, many=True, request=request).data
            })
        all_data[BrakeTypeSerializer.Meta.model._meta.model_name] = data

        # 制动盘
        queryset = BrakeDiscType.objects.all()
        all_data[BrakeDiscTypeListSerializer.Meta.model._meta.model_name] = {
            "total": queryset.count(),
            "data": BrakeDiscTypeListSerializer(instance=queryset, many=True, request=request).data
        }

        # 闸片/闸瓦
        queryset = PadType.objects.all()
        all_data[PadTypeListSerializer.Meta.model._meta.model_name] = {
            "total": queryset.count(),
            "data": PadTypeListSerializer(instance=queryset, many=True, request=request).data
        }

        return SuccessResponse(data=all_data, msg="获取成功")
