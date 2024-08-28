from dvadmin.system.views.message_center import MessageCenterCreateSerializer


def send_message(data, request=None):
    msg_serializer = MessageCenterCreateSerializer(data=data)
    msg_serializer.is_valid(raise_exception=True)
    msg_serializer.save()
