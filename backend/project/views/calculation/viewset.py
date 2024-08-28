from dvadmin.utils.json_response import SuccessResponse
from dvadmin.utils.viewset import CustomModelViewSet
from project.views.calculation.service.one_step_calculation import *
# noinspection PyUnusedLocal
class EclipseCalculation(CustomModelViewSet):
    """
    项目报告接口
    """
    def one_setp(self, request, *args, **kwargs):
        json_data = request.data
        print(type(json_data))
        onstepCalculationSystem=BXCalculationSystem(json_data)
        result=OneStepCalculation(onstepCalculationSystem).calculation_results()
        return SuccessResponse(result)
