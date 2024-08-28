# 初始化
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "application.settings")
django.setup()

from dvadmin.utils.core_initialize import CoreInitialize
from project.serializers.initialize_serializers import (
    ProjectPadTypeInitSerializer,
    ProjectDiscTypeInitSerializer,
    ProjectBrakeTypeInitSerializer,
    ProjectBrakeInitSerializer,
    ProjectBasicElementInitSerializer,
    ProjectCarInitSerializer,
    ProjectBrakeDiscInitSerializer,
    ProjectBrakeLiningShoeInitSerializer,
    ProjectValveInitSerializer,
    ProjectMTBInitSerializer
)


class Initialize(CoreInitialize):

    def init_pad_type(self):
        """
        初始化闸片闸瓦类型数据
        """
        self.init_base(ProjectPadTypeInitSerializer, unique_fields=['name'])
    
    def init_brake_lining_shoe(self):
        """
        初始化闸片闸瓦数据（假数据）
        """
        # self.init_base(ProjectBrakeLiningShoe, unique_fields=['item', 'type_of_pad'])
        self.init_base(ProjectBrakeLiningShoeInitSerializer, unique_fields=['item'])

    def init_disc_type(self):
        """
        初始化制动盘类型数据
        """
        self.init_base(ProjectDiscTypeInitSerializer, unique_fields=['name'])

    def init_brake_disc(self):
        """
        初始化制动盘数据（假数据）
        """
        # self.init_base(ProjectBrakeDiscInitSerializer, unique_fields=['item', 'type_of_disc'])
        self.init_base(ProjectBrakeDiscInitSerializer, unique_fields=['item'])

    def init_brake_type(self):
        """
        初始化制动器类型数据
        """
        # self.init_base(ProjectBrakeTypeInitSerializer, unique_fields=['name', 'type_of_brake'])
        self.init_base(ProjectBrakeTypeInitSerializer, unique_fields=['name'])

    def init_brake(self):
        """
        初始化制动器数据（假数据）
        """
        # self.init_base(ProjectBrakeInitSerializer, unique_fields=['item', 'brake_type'])
        self.init_base(ProjectBrakeInitSerializer, unique_fields=['item'])


    def init_basic_element(self):
        """
        初始化基础部件数据
        """
        self.init_base(ProjectBasicElementInitSerializer, unique_fields=['name'])

    def init_car(self):
        """
        初始化车辆部件数据
        """
        self.init_base(ProjectCarInitSerializer, unique_fields=['name', 'car_type'])

    def init_Valve(self):
        """
        初始化调整阀数据
        """
        # self.init_base(ProjectValveInitSerializer, unique_fields=['item', 'mode'])
        self.init_base(ProjectValveInitSerializer, unique_fields=['item'])

    def init_mtb(self):
        """
        初始化MTB数据
        """
        # self.init_base(ProjectMTBInitSerializer, unique_fields=['item', 'mtb_type'])
        self.init_base(ProjectMTBInitSerializer, unique_fields=['item'])

    def run(self):
        self.init_pad_type()
        self.init_brake_lining_shoe()
        self.init_disc_type()
        self.init_brake_disc()
        self.init_brake_type()
        self.init_brake()
        self.init_basic_element()
        self.init_car()
        self.init_Valve()
        self.init_mtb()


if __name__ == "__main__":
    Initialize(app='project').run()
