from django.conf import settings
from rest_framework.exceptions import APIException

from dvadmin.system.models import Users, Role
from dvadmin.utils.json_response import DetailResponse, SuccessResponse, ErrorResponse

from dvadmin.utils.viewset import CustomModelViewSet
from project.views.message import send_message
from project.serializers.project import (

    ProjectCheckerSerializer
)


class ProjectCheckerViewSet(CustomModelViewSet):
    """
    获取审核人列表接口
    """
    serializer_class = ProjectCheckerSerializer

    def list(self, request, *args, **kwargs):
        key = request.query_params.get("key", "")
        if key:
            queryset = Users.objects.filter(role__key=key)
            datas = self.get_serializer(queryset, many=True, request=request).data
        else:
            datas = {}
            for i in settings.PROJECT_CHECK_ROLE:
                queryset = Users.objects.filter(role__key=i)
                datas[i] = self.get_serializer(queryset, many=True, request=request).data
        return SuccessResponse(data=datas, msg="获取成功")

