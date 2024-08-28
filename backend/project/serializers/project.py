from rest_framework import serializers


from dvadmin.system.models import Users
from dvadmin.utils.serializers import CustomModelSerializer

# 审核人
class ProjectCheckerSerializer(CustomModelSerializer):
    """
    审核人序列化器
    """

    class Meta:
        model = Users
        read_only_fields = ["id"]
        fields = ["username", "name", "id"]
        extra_kwargs = {
            "post": {"required": False},
        }
