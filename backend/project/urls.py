from django.urls import path

from project.views.project.project_check import ProjectCheckerViewSet

from project.views.unit.unit import AllUnitViewSet, AllUnitTypeViewSet
from project.views.unit.unit_brake import BrakeViewSet, BrakeTypeViewSet
from project.views.unit.unit_brakedisc import BrakeDiscViewSet, BrakeDiscTypeViewSet
from project.views.unit.unit_brakeliningshoe import PadViewSet, PadTypeViewSet
from project.views.unit.unit_check import UnitCheckViewSet
from project.views.unit.unit_mtb import MTBViewSet
from project.views.unit.unit_valve import ValveViewSet

from project.views.unit_manage.unit_brake import BrakeManagementViewSet
from project.views.unit_manage.unit_brakedisc import BrakeDiscManagementViewSet
from project.views.unit_manage.unit_brakepad import BrakeLiningShoeManagementViewSet
from project.views.unit_manage.unit_type import BrakeDiscTypeManagementViewSet, PadTypeManagementViewSet
from project.views.unit_manage.unit_valve import ValveManagementViewSet
from project.views.unit_manage.unit_mtb import MTBManagementViewSet

from project.views.calculation.viewset import EclipseCalculation

urlpatterns = [
    # 项目
    path('project_checker/', ProjectCheckerViewSet.as_view({'get': 'list'})),
    # 项目部件
    path('unit/all/', AllUnitViewSet.as_view({'get': 'list'})),
    path('unit/alltype/', AllUnitTypeViewSet.as_view({'get': 'list'})),

    path('unit/brake/', BrakeViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('unit/brake/<int:pk>/', BrakeViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('unit/braketype/', BrakeTypeViewSet.as_view({'get': 'list'})),
    path('unit/brake/search/', BrakeViewSet.as_view({'get': 'search_list'})),
    path('unit/brake/createfields/', BrakeViewSet.as_view({'get': 'create_fields'})),

    path('unit/brakedisc/', BrakeDiscViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('unit/brakedisc/<int:pk>/', BrakeDiscViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('unit/brakedisctype/', BrakeDiscTypeViewSet.as_view({'get': 'list'})),
    path('unit/brakedisc/search/', BrakeDiscViewSet.as_view({'get': 'search_list'})),
    path('unit/brakedisc/createfields/', BrakeDiscViewSet.as_view({'get': 'create_fields'})),

    path('unit/pad/', PadViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('unit/pad/<int:pk>/', PadViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('unit/padtype/', PadTypeViewSet.as_view({'get': 'list'})),
    path('unit/pad/search/', PadViewSet.as_view({'get': 'search_list'})),
    path('unit/pad/createfields/', PadViewSet.as_view({'get': 'create_fields'})),

    path('unit/valve/', ValveViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('unit/valve/<int:pk>/', ValveViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('unit/valve/search/', ValveViewSet.as_view({'get': 'search_list'})),
    path('unit/valve/createfields/', ValveViewSet.as_view({'get': 'create_fields'})),

    path('unit/mtb/', MTBViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('unit/mtb/<int:pk>/', MTBViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('unit/mtb/search/', MTBViewSet.as_view({'get': 'search_list'})),
    path('unit/mtb/createfields/', MTBViewSet.as_view({'get': 'create_fields'})),


    # 管理部件
    path('unit/management/brake/', BrakeManagementViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('unit/management/brake/<int:pk>/', BrakeManagementViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('unit/management/brake/createfields/', BrakeManagementViewSet.as_view({'get': 'create_fields'})),

    path('unit/management/brakedisc/', BrakeDiscManagementViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('unit/management/brakedisc/<int:pk>/', BrakeDiscManagementViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('unit/management/brakedisc/createfields/', BrakeDiscManagementViewSet.as_view({'get': 'create_fields'})),

    path('unit/management/pad/', BrakeLiningShoeManagementViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('unit/management/pad/<int:pk>/', BrakeLiningShoeManagementViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('unit/management/pad/createfields/', BrakeLiningShoeManagementViewSet.as_view({'get': 'create_fields'})),

    path('unit/management/valve/', ValveManagementViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('unit/management/valve/<int:pk>/', ValveManagementViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('unit/management/valve/createfields/', ValveManagementViewSet.as_view({'get': 'create_fields'})),

    path('unit/management/mtb/', MTBManagementViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('unit/management/mtb/<int:pk>/', MTBManagementViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('unit/management/mtb/createfields/', MTBManagementViewSet.as_view({'get': 'create_fields'})),

    path('unit/management/brakedisc/type/', BrakeDiscTypeManagementViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('unit/management/brakedisc/type/<int:pk>/', BrakeDiscTypeManagementViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    path('unit/management/pad/type/', PadTypeManagementViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('unit/management/pad/type/<int:pk>/', PadTypeManagementViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),


    # 部件审核
    path('unit_check/', UnitCheckViewSet.as_view({'get': 'list'})),
    path('unit_check/<int:pk>/', UnitCheckViewSet.as_view({'get': 'retrieve', 'put': 'check'})),
    # calculation
    path('one_step/', EclipseCalculation.as_view({'post': 'one_setp'})),
]
