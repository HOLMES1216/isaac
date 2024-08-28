from django.conf import settings
from rest_framework import serializers

from project.models import (
    PadType, BrakeDiscType,
    BrakeType, Brake,
    BasicElement,
    Car, BrakeDisc,
    BrakeLiningShoe,
    Valve, MTB
)

from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.validator import CustomValidationError




class ProjectPadTypeInitSerializer(CustomModelSerializer):
    """
    闸片闸瓦类型初始化 序列化器
    """

    class Meta:
        model = PadType
        fields = ["name", "area_per_disc", "height_of_wear", "alpha_pad", "beta_pad", "gamma_pad", "efficiency_of_disc"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "creator": {"write_only": True},
            "dept_belong_id": {"write_only": True}
        }


class ProjectBrakeLiningShoeInitSerializer(CustomModelSerializer):
    """
    闸片闸瓦数据初始化 序列化器
    """
    pad_type = serializers.CharField()

    def validate_pad_type(self, attr):
        try:
            ins = PadType.objects.get(name=attr)
        except:
            raise CustomValidationError(f"The pad type '{attr}' is not exists.")
        return ins

    class Meta:
        model = BrakeLiningShoe
        fields = ["pad_type", "type_of_pad", "item", "img", "is_global", "item_name", "alpha_pad", "pad_thickness",
                  "pad_shape", "width", "length", "thickness", "wearlimit"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "creator": {"write_only": True},
            "dept_belong_id": {"write_only": True}
        }


class ProjectDiscTypeInitSerializer(CustomModelSerializer):
    """
    制动盘类型初始化 序列化器
    """

    class Meta:
        model = BrakeDiscType
        fields = ["name", "density_of_material", "modulus_of_elasticity", "poissons_ratio",
                  "max_allowed_puls_bending_stress", "coeff_of_thermal_expansion_alpha",
                  "coeff_of_thermal_conduction_at_0_c", "first_deriv_of_ctc_at_0_c",
                  "specific_heat_capacity_at_0_c", "first_deriv_of_the_shc_at_0_c",
                  "radiation_coeff_of_friction_surface", "radiation_coeff_of_cooling_surface"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "creator": {"write_only": True},
            "dept_belong_id": {"write_only": True}
        }


class ProjectBrakeDiscInitSerializer(CustomModelSerializer):
    """
    制动盘数据初始化 序列化器
    """
    disc_type = serializers.CharField()

    def validate_disc_type(self, attr):
        try:
            ins = BrakeDiscType.objects.get(name=attr)
        except:
            raise CustomValidationError(f"The brake disc type '{attr}' is not exists.")
        return ins

    class Meta:
        model = BrakeDisc
        fields = ["disc_type", "type_of_disc", "item", "img", "is_global", "inner_diameter", "outer_diameter",
                  "thickness_of_the_friction_ring", "free_convection", "cooling_constant_cek", "cooling_constant_sigma",
                  "reduction_of_convection_c1k", "number_of_ribs", "thickness_of_the_ribs", "thickness_of_the_disc",
                  "bf", "reib", "screw_envelope_outer_diameter"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "creator": {"write_only": True},
            "dept_belong_id": {"write_only": True}
        }


class ProjectBrakeTypeInitSerializer(CustomModelSerializer):
    """
    制动器类型初始化 序列化器
    """

    class Meta:
        model = BrakeType
        fields = ["name", "type_of_brake"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "create": {"write_only": True},
            "dept_belong_id": {"write_only", True}
        }


class ProjectBrakeInitSerializer(CustomModelSerializer):
    """
    制动器初始化 序列化器
    """
    brake_type = serializers.CharField()

    def validate_brake_type(self, attr):
        try:
            ins = BrakeType.objects.get(name=attr)
        except:
            raise CustomValidationError(f"The brake type '{attr}' is not exists.")
        return ins

    class Meta:
        model = Brake
        fields = ["brake_type", "item", "img", "is_global", "cylinder_area", "cylinder_efficiency", "cylinder_ratio",
                  "cylinder_spring_force", "rigging_efficiency", "rigging_ratio", "transmission_efficiency",
                  "transmission_ratio", "brake_pad_area", "number_of_pad_per_brake_cylinder",
                  "friction_area_of_the_disc", "pressure_limit", "pb_force", "lever_length", "lever_length_the_front",
                  "offset_pull_rod_rotation_point_in_lever", "pad_holder_height", "wear_of_lever_bolt",
                  "wear_of_pad_holder_bolt", "distance_cylinder_fixation_yoke_fixation", "pre_adjustment_in_cylinder",
                  "gdimension", "hanger_upper_bolt_to_lower_bolt", "hanger_lower_bolt_to_pad_holder_assemble_surface",
                  "dis_between_hanger_upper_bolt", "hanger_upper_bolt_to_caliper_center",
                  "hanger_lower_bolt_to_pad_center", "ll", "lr", "lr1", "lr2", "d1", "d2", "d3", "h1", "h2", "h3", "h4",
                  "rigging_spring_force"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "create": {"write_only": True},
            "dept_belong_id": {"write_only", True}
        }


# class ProjectControlPlatformInitSerializer(CustomModelSerializer):
#     """
#     控制系统平台初始化 序列化器
#     """

#     class Meta:
#         model = ControlPlatform
#         fields = ["system", "version"]
#         read_only_fields = ["id"]
#         extra_kwargs = {
#             "create": {"write_only": True},
#             "dept_belong_id": {"write_only", True}
#         }


class ProjectBasicElementInitSerializer(CustomModelSerializer):
    """
    基础部件初始化 序列化器
    """

    class Meta:
        model = BasicElement
        fields = ["name", "img", "detail"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "create": {"write_only": True},
            "dept_belong_id": {"write_only", True}
        }


class ProjectCarInitSerializer(CustomModelSerializer):
    """
    基础部件初始化 序列化器
    """

    class Meta:
        model = Car
        fields = ["car_type", "name", "img", "detail"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "create": {"write_only": True},
            "dept_belong_id": {"write_only", True}
        }


class ProjectValveInitSerializer(CustomModelSerializer):
    """
    调整阀初始化 序列化器
    """

    class Meta:
        model = Valve
        fields = ["mode", "item", "img", "is_global", "c_0_high", "c_100_high", "aw_0", "aw_100", "c_apply", "t_0",
                  "t_100", "c_max", "factor_f2p", "f_apply", "rv_factor", "high_low", "c_max_nb", "edu_offset",
                  "a_0_high", "a_100_high", "cv_max_sb", "v_switch_h_l", "c_0_low", "c_100_low", "a_0_low", "a_100_low"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "create": {"write_only": True},
            "dept_belong_id": {"write_only", True}
        }


class ProjectMTBInitSerializer(CustomModelSerializer):
    """
    MTB初始化 序列化器
    """

    class Meta:
        model = MTB
        fields = ["mtb_type", "item", "img", "is_global", "v_max", "step", "v_off", "total_actractive_force",
                  "efficiency", "curve_data"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "create": {"write_only": True},
            "dept_belong_id": {"write_only", True}
        }
