import django_filters
from rest_framework.exceptions import APIException, PermissionDenied

from project.models import UnitCheck, Brake, BrakeDisc, BrakeLiningShoe, MTB, Valve
from dvadmin.system.models import Users
from dvadmin.utils.json_response import ErrorResponse, DetailResponse
from dvadmin.utils.viewset import CustomModelViewSet


# 过滤器
class BrakeFilter(django_filters.FilterSet):
    type_of = django_filters.NumberFilter(field_name='brake_type__type_of_brake')
    # type_of = django_filters.NumberFilter(method='get_type_of')

    # def get_type_of(self, queryset, key, value):
    #     datas = queryset.filter(brake_type__type_of_brake=value)
    #     return datas

    class Meta:
        model = Brake
        fields = ['type_of']


class BrakeDiscFilter(django_filters.FilterSet):
    type_of = django_filters.NumberFilter(field_name='type_of_disc')

    class Meta:
        model = BrakeDisc
        fields = ['type_of']


class BrakePadFilter(django_filters.FilterSet):
    type_of = django_filters.NumberFilter(field_name='type_of_pad')

    class Meta:
        model = BrakeLiningShoe
        fields = ['type_of']


class ValveFilter(django_filters.FilterSet):
    type_of = django_filters.NumberFilter(field_name='mode')

    class Meta:
        model = Valve
        fields = ['type_of']


class MTBFilter(django_filters.FilterSet):
    type_of = django_filters.NumberFilter(field_name='mtb_type')

    class Meta:
        model = MTB
        fields = ['type_of']


# 公用视图集
class CommonViewSet(CustomModelViewSet):
    """
    公用视图集
    """
    search_fields = ['item']
    MODEL = None
    UNIT_CLASS = None

    # def get_queryset(self):
    #     if self.request.user.is_superuser:
    #         return super().get_queryset()
    #     return []

    def get_object(self):
        if self.MODEL is None:
            raise Exception("Please override the 'MODEL' property")
        queryset = self.MODEL.objects.filter(**self.kwargs)
        if not queryset.exists():
            raise APIException("Data is not exists.")
        return queryset.first()

    def get_queryset(self):
        return self.MODEL.objects.all()

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

    def permission_check(self, rolename):
        if self.request.user.is_superuser:
            return
        if rolename not in self.request.user.role.values_list('name', flat=True):
            raise PermissionDenied('You not have permission to visit.')

    def create_item_check(self, item):
        """新增的时候判断item是否被占用"""
        if self.MODEL.objects.filter(item=item).exists():
            raise APIException("The item '%s' is exists." % item)

    def update_item_check(self, old_item, new_item):
        """编辑的时候判断item是否被占用"""
        if new_item != old_item and self.MODEL.objects.filter(item=new_item).exists():
            raise APIException("The item '%s' is exists." % new_item)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.project:
            return ErrorResponse(msg="You cannot delete a unit that is bound to a project.")
        if instance.is_global:
            return ErrorResponse(msg="You cannot delete global unit.")
        if not self.request.user.is_superuser:
            return ErrorResponse(msg="You dosen't have permission to delete this unit.")
        self.perform_destroy(instance)
        return DetailResponse(data=[], msg="删除成功")

    def create_check(self, unit, checker):
        if (i := UnitCheck.objects.filter(
            unit_class=self.UNIT_CLASS,
            unit=unit.pk,
            state=0
        )):
            i.delete()
        UnitCheck.objects.create(
            unit_class=self.UNIT_CLASS,
            unit=unit.pk,
            checker=checker,
            creator=self.request.user
        )

    def get_matching_serializer(self, *args, **kwargs):
        raise NotImplementedError('You must override the function!')

    def create_fields(self, request, *args, **kwargs):
        raise NotImplementedError('You must override the function!')

    def create(self, request, *args, **kwargs):
        raise NotImplementedError('You must override the function!')

    def update(self, request, *args, **kwargs):
        raise NotImplementedError('You must override the function!')

    def retrieve(self, request, *args, **kwargs):
        raise NotImplementedError('You must override the function!')

    def get_checker(self, pk):
        # 获取审核人
        return Users.objects.get(pk=pk)
