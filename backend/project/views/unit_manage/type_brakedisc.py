from dvadmin.utils.viewset import CustomModelViewSet
from project.models import BrakeDiscType
from project.serializers.unit import BrakeDiscTypeSerializer


class BrakeDiscTypeViewSet(CustomModelViewSet):
    serializer_class = BrakeDiscTypeSerializer
    queryset = BrakeDiscType.objects.all()
