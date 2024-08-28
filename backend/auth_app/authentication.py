from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomJWTAuthentication(JWTAuthentication):
    def get_header(self, request):
        # 这里可以自定义获取JWT令牌的逻辑，例如从不同的HTTP头部获取
        # 例如，您可以从自定义的HTTP头部 'Authorization_dvadmin' 获取令牌
        # 确保请求头部名称与实际发送的令牌头部名称一致
        header = request.headers.get('Authorizationnew')
        return header

    def authenticate(self, request):
        # 获取JWT令牌
        header = self.get_header(request)
        if header is None:
            # print(f"No JWT authentication")
            return None

        # 尝试解析JWT令牌
        try:
            # 这里使用JWT库的decode方法来验证和解码令牌
            # 您可能需要根据您的项目配置调整decode方法的参数
            parts = header.split()
            token = parts[1]
            validated_token = self.get_validated_token(token)

            # 获取用户
            user = self.get_user(validated_token)

            # 如果用户存在，则返回用户和令牌
            if user is not None:
                return (user, validated_token)

        except Exception as e:
            # 这里可以记录异常信息，例如打印或记录日志
            print(f"Error during JWT authentication: {e}")

        # 如果认证失败，返回None
        return None