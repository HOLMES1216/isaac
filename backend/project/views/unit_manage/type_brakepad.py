from dvadmin.utils.viewset import CustomModelViewSet
from project.models import PadType
from project.serializers.unit import PadTypeSerializer


class BrakePadTypeViewSet(CustomModelViewSet):
    serializer_class = PadTypeSerializer
    queryset = PadType.objects.all()
