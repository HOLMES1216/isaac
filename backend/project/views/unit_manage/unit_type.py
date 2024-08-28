from rest_framework.exceptions import APIException

from project.models import BrakeDiscType, PadType, BrakeDisc, BrakeLiningShoe
from project.serializers.unit import (
    BrakeDiscTypeUpdateManagementSerializer,
    BrakeDiscTypePostManagementSerializer,
    BrakeDiscTypeListManagementSerializer,
    PadTypeUpdateManagementSerializer,
    PadTypePostManagementSerializer,
    PadTypeListManagementSerializer
)
from dvadmin.utils.json_response import ErrorResponse, DetailResponse
from dvadmin.utils.viewset import CustomModelViewSet


class CommonViewSet(CustomModelViewSet):
    """
    公共视图集
    """
    list_serializer = None
    create_serializer = None
    update_serializer = None
    MODEL = None

    def get_queryset(self):
        return self.MODEL.objects.all()

    def get_object(self):
        queryset = self.get_queryset().filter(**self.kwargs)
        if not queryset.exists():
            raise APIException("Data is not exists.")
        return queryset.first()

    def get_serializer_class(self):
        if self.action == 'list':
            return self.list_serializer
        elif self.action == 'retrieve':
            return self.create_serializer
        elif self.action == 'create':
            return self.create_serializer
        elif self.action == 'update':
            return self.update_serializer
        return self.list_serializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        if data.get('name', None) is None:
            return ErrorResponse(msg="The name must be passed.")
        if self.get_queryset().filter(name=data.get('name')).exists():
            return ErrorResponse(msg="The name '%s' is exists." % data.get('name'))
        return super().create(request, *args, **kwargs)

    # def update(self, request, *args, **kwargs):
    #     if request.data.get('name', None) is not None:
    #         return ErrorResponse(msg="Cannot change the name.")
    #     return super().update(request, *args, **kwargs)


class BrakeDiscTypeManagementViewSet(CommonViewSet):
    """
    制动盘类型管理的增删改查
    """
    list_serializer = BrakeDiscTypeListManagementSerializer
    create_serializer = BrakeDiscTypePostManagementSerializer
    update_serializer = BrakeDiscTypeUpdateManagementSerializer
    MODEL = BrakeDiscType

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if BrakeDisc.objects.filter(disc_type=instance.pk).exists():
            return ErrorResponse(msg="You cannot delete a type that is bound to a unit.")
        instance.delete()
        return DetailResponse(data=[], msg="删除成功")


class PadTypeManagementViewSet(CommonViewSet):
    """
    闸片闸瓦类型管理的增删改查
    """
    list_serializer = PadTypeListManagementSerializer
    create_serializer = PadTypePostManagementSerializer
    update_serializer = PadTypeUpdateManagementSerializer
    MODEL = PadType

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if BrakeLiningShoe.objects.filter(pad_type=instance.pk).exists():
            return ErrorResponse(msg="You cannot delete a type that is bound to a unit.")
        instance.delete()
        return DetailResponse(data=[], msg="删除成功")
