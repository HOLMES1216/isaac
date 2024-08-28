from rest_framework.exceptions import APIException

from project import models
from project.serializers import unit as unit_serializers
from project.serializers.unit import (
    MTBSerializer,
    TreadBrakeAllSerializer,
    OtherWheelAxleBrakeAllSerializer,
    RZWheelWZAxleBrakeAllSerializer,
    WheelBrakeDiscAllSerializer,
    AxleBrakeDiscAllSerializer,
    BrakeShoeAllSerializer,
    BrakeLiningAllSerializer,
    EDUHLValveSerializer,
    EDUValveSerializer,
    RVValveSerializer,
    ALL_FIELDS_DICT
)
from dvadmin.utils.json_response import ErrorResponse, DetailResponse
from dvadmin.utils.viewset import CustomModelViewSet


class UnitCheckViewSet(CustomModelViewSet):
    """
    部件审核 视图集
    """
    serializer_class = unit_serializers.UnitCheckSerializer

    def __init__(self, *args, **kwargs):
        self.serializer_pattern = {
            'Brake': lambda ins: self.brake_serializer(ins.brake_type.type_of_brake, ins.brake_type.name),
            'BrakeDisc': lambda ins: self.brakedisc_serializer(ins.type_of_disc),
            'BrakeLiningShoe': lambda ins: self.brakeliningshoe_serializer(ins.type_of_pad),
            'Valve': lambda ins: self.valve_serializer(ins.mode, ins.high_low),
            'MTB': lambda ins: self.mtb_serializer()
        }
        super().__init__(*args, **kwargs)

    def brake_serializer(self, type_of_brake, brake_type_name):
        serializer = None
        opt = ("RZ", "WZ")
        if type_of_brake in [0, 1]:  # 轮装/轴装
            if brake_type_name == opt[type_of_brake]:  # RZ/WZ类型
                serializer = RZWheelWZAxleBrakeAllSerializer
            else:  # 其他类型
                serializer = OtherWheelAxleBrakeAllSerializer
        elif type_of_brake == 2:  # 踏面
            serializer = TreadBrakeAllSerializer
        return serializer

    def brakedisc_serializer(self, type_of_disc):
        serializer = None
        if type_of_disc == 0:  # 轮装
            serializer = WheelBrakeDiscAllSerializer
        elif type_of_disc == 1:  # 轴装
            serializer = AxleBrakeDiscAllSerializer
        return serializer

    def brakeliningshoe_serializer(self, type_of_pad):
        serializer = None
        if type_of_pad == 0:  # 闸片
            serializer = BrakeLiningAllSerializer
        elif type_of_pad == 1:  # 闸瓦
            serializer = BrakeShoeAllSerializer
        return serializer

    def valve_serializer(self, mode, high_low):
        serializer = None
        if mode == 1:  # EDU
            if high_low:  # High/Low为True
                serializer = EDUHLValveSerializer
            else:  # High/Low为False
                serializer = EDUValveSerializer
        elif mode == 0:  # RV
            serializer = RVValveSerializer
        return serializer

    def mtb_serializer(self):
        return MTBSerializer

    def get_matching_serializer(self, unit_class, instance):
        if unit_class in self.serializer_pattern:
            serializer = self.serializer_pattern[unit_class](instance)
            print("%s serializer is" % unit_class, serializer)
            return serializer
        else:
            raise APIException("unit_class '%s' is not exists" % unit_class)

    def get_matching_field(self, unit_class, serializer):
        fields = list(set(ALL_FIELDS_DICT[unit_class]) - set(serializer.Meta.exclude))
        fields.sort()
        return fields

    def get_queryset(self):
        if self.request.user.is_superuser:
            qs = models.UnitCheck.objects.all()
        else:
            qs = models.UnitCheck.objects.filter(checker=self.request.user.pk)
        return qs

    def get_object(self):
        res = self.get_queryset().filter(pk=self.kwargs.get('pk')).first()
        if res:
            return res
        raise APIException('This record is not exists.')

    def check(self, request, *args, **kwargs):
        data = request.data.copy()
        instance = self.get_object()
        if not self.request.user.is_superuser:
            if self.request.user.pk != instance.checker.pk:
                return ErrorResponse(msg='You cannot check this record.')
        result = data.get('result', '')
        if result == '':
            return ErrorResponse(msg='Please submit the check result.')
        result = bool(int(result))
        if instance.state:
            return ErrorResponse(msg='This record has been checked.')
        if result:
            instance.state = 1
        else:
            instance.state = 2
        instance.save()
        return DetailResponse(msg='操作成功')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        unit_class = instance.get_unit_class_display()
        obj = getattr(models, unit_class).objects.get(pk=instance.unit)
        serializer = self.get_matching_serializer(unit_class, obj)
        fields = self.get_matching_field(unit_class, serializer)
        if serializer is None:
            return ErrorResponse('No matching serializer was found.')
        serializer = serializer(instance=obj, request=request)
        data = {
            "detail": serializer.data,
            "fields": fields,
            "field_count": len(fields)
        }
        return DetailResponse(data=data, msg='获取成功')
