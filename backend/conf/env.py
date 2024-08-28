import os

from application.settings import BASE_DIR



# ================================================= #
# *************** mysql数据库 配置  *************** #
# ================================================= #
# 使用mysql时，改为此配置
DATABASE_ENGINE = "django.db.backends.mysql"
DATABASE_NAME = 'isaac-dvadmin-test-simbrake' # mysql 时使用

# 数据库地址 改为自己数据库地址
# DATABASE_HOST = 'dvadmin3-mysql'
DATABASE_HOST = '10.131.69.20'
# # 数据库端口
DATABASE_PORT = 3306
# # 数据库用户名
DATABASE_USER = "root"
# # 数据库密码
DATABASE_PASSWORD = "123321holmes"
# 5. Execute the migration command:
#  python manage.py makemigrations
#  python manage.py migrate
# 6. Initialization data
#  python manage.py init
# ================================================= #
# *************** Test mysql数据库 配置  *************** #
# ================================================= #
# 使用mysql时，改为此配置
DATABASE_ENGINE_TEST = "django.db.backends.mysql"
DATABASE_NAME_TEST = 'isaac-dev-test' # mysql 时使用

# 数据库地址 改为自己数据库地址
# DATABASE_HOST = 'dvadmin3-mysql'
DATABASE_HOST_TEST = '10.131.69.20'
# # 数据库端口
DATABASE_PORT_TEST = 3306
# # 数据库用户名
DATABASE_USER_TEST = "root"
# # 数据库密码
DATABASE_PASSWORD_TEST = "123321holmes"


# 表前缀
TABLE_PREFIX = "isaac_test_"
# ================================================= #
# ******** redis配置，无redis 可不进行配置  ******** #
# ================================================= #
REDIS_PASSWORD = 'DVADMIN3'
# REDIS_HOST = 'dvadmin3-redis'
REDIS_HOST = 'mucs70737'
REDIS_URL = f'redis://:{REDIS_PASSWORD or ""}@{REDIS_HOST}:6379'
REDIS_URL_CHANNEL = f'redis://:{REDIS_PASSWORD or ""}@{REDIS_HOST}/0'
CACHES = { # 配置缓存
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"{REDIS_URL}/1", # 库名可自选1~16
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}
BROKER_URL = f"{REDIS_URL}/2" # 库名可自选1~16
RESULT_BACKEND = f"{REDIS_URL}/3" # 库名可自选1~16
CELERY_RESULT_BACKEND = f"{REDIS_URL}/4" # celery结果存储到数据库中
# CELERY_RESULT_BACKEND ='django-db'
# CELERYBEAT_SCHEDULER = "django_celery_beat.schedulers.DatabaseScheduler"  # Backend数据库
#避免时区的问题
CELERY_ENABLE_UTC = False
DJANGO_CELERY_BEAT_TZ_AWARE = False
CELERY_TASK_TIME_LIMIT = 180

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [
                "redis://:DVADMIN3@dvadmin3-redis/0"
            ],
            'capacity': 1500,
            'expiry': 20,
        }
    }
}

WEBSOCKET_MAX_MESSAGE_SIZE = 10*1024*1024

# ================================================= #
# ****************** 功能 启停  ******************* #
# ================================================= #
DEBUG = True
# 启动登录详细概略获取(通过调用api获取ip详细地址。如果是内网，关闭即可)
ENABLE_LOGIN_ANALYSIS_LOG = True
# 登录接口 /api/token/ 是否需要验证码认证，用于测试，正式环境建议取消
LOGIN_NO_CAPTCHA_AUTH = True
# ================================================= #
# ****************** 其他 配置  ******************* #
# ================================================= #

ALLOWED_HOSTS = ["*"]
# 列权限中排除App应用
COLUMN_EXCLUDE_APPS = []
