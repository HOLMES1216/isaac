from rest_framework import serializers

from project.models import (
    BasicElement,
    Car,
    BrakeType,
    Brake,
    BrakeDiscType,
    BrakeDisc,
    PadType,
    BrakeLiningShoe,
    Valve,
    MTB,
    UnitCheck
)
from dvadmin.utils.serializers import CustomModelSerializer


class BasicElementSerializer(CustomModelSerializer):
    """
    基础部件 序列化器
    """
    label = serializers.SerializerMethodField()

    def get_label(self, obj):
        return "Basic Element"

    class Meta:
        model = BasicElement
        read_only_fields = ["id"]
        exclude = ["is_deleted"]


# 车辆
class CarSerializer(CustomModelSerializer):
    """
    车辆部件 序列化器
    """
    label = serializers.SerializerMethodField()

    def get_label(self, obj):
        return "Car"

    class Meta:
        model = Car
        read_only_fields = ["id"]
        exclude = ["is_deleted"]


# 制动器
class BrakeTypeSerializer(CustomModelSerializer):
    """
    制动器类型(轮装/轴装/踏面) 序列化器
    """

    class Meta:
        model = BrakeType
        read_only_fields = ["id"]
        exclude = ["is_deleted"]


class RZWheelWZAxleBrakeAllSerializer(CustomModelSerializer):
    """
    RZ和WZ类型的轮装/轴装制动器 序列化器
    BES2,BES3和超管可用
    """
    type_of_brake = serializers.SerializerMethodField()
    # main_type = serializers.SerializerMethodField()

    def get_type_of_brake(self, obj):
        return obj.brake_type.type_of_brake

    # def get_main_type(self, obj):
    #     return obj.brake_type.get_type_of_brake_display()

    class Meta:
        model = Brake
        read_only_fields = ["id"]
        exclude = ["is_deleted", "ll", "lr", "lr1", "lr2", "d1", "d2", "d3", "h1", "h2", "h3", "h4",
                   "rigging_spring_force"]


class OtherWheelAxleBrakeAllSerializer(CustomModelSerializer):
    """
    其他类型的轮装/轴装制动器 序列化器
    BES2,BES3和超管可用
    """
    type_of_brake = serializers.SerializerMethodField()
    # main_type = serializers.SerializerMethodField()

    def get_type_of_brake(self, obj):
        return obj.brake_type.type_of_brake

    # def get_main_type(self, obj):
    #     return obj.brake_type.get_type_of_brake_display()

    class Meta:
        model = Brake
        read_only_fields = ["id"]
        exclude = ["is_deleted", "lever_length", "lever_length_the_front", "offset_pull_rod_rotation_point_in_lever",
                   "pad_holder_height", "wear_of_lever_bolt", "wear_of_pad_holder_bolt",
                   "distance_cylinder_fixation_yoke_fixation", "pre_adjustment_in_cylinder", "gdimension",
                   "hanger_upper_bolt_to_lower_bolt", "hanger_lower_bolt_to_pad_holder_assemble_surface",
                   "dis_between_hanger_upper_bolt", "hanger_upper_bolt_to_caliper_center",
                   "hanger_lower_bolt_to_pad_center", "rigging_spring_force"]


class WheelAxleBrakeMSESerializer(CustomModelSerializer):
    """
    轮转轴装制动器 序列化器
    MSE可用
    """

    class Meta:
        model = Brake
        read_only_fields = ["id"]
        exclude = list(set(RZWheelWZAxleBrakeAllSerializer.Meta.exclude + OtherWheelAxleBrakeAllSerializer.Meta.exclude))


class BrakePartSerializer(CustomModelSerializer):
    """
    轮装轴装制动器 序列号器
    可看字段最少的用户可用
    """

    class Meta:
        model = Brake
        read_only_fields = ["id"]
        exclude = list(set(
            RZWheelWZAxleBrakeAllSerializer.Meta.exclude + OtherWheelAxleBrakeAllSerializer.Meta.exclude
        )) + ["cylinder_area", "cylinder_efficiency", "cylinder_ratio", "cylinder_spring_force", "rigging_efficiency",
              "rigging_ratio", "transmission_efficiency", "transmission_ratio", "brake_pad_area",
              "number_of_pad_per_brake_cylinder", "friction_area_of_the_disc", "pressure_limit", "pb_force"]


class TreadBrakeAllSerializer(CustomModelSerializer):
    """
    踏面制动器 序列化器
    MSE,BES3和超管可用
    """
    type_of_brake = serializers.SerializerMethodField()
    # main_type = serializers.SerializerMethodField()

    def get_type_of_brake(self, obj):
        return obj.brake_type.type_of_brake

    # def get_main_type(self, obj):
    #     return obj.brake_type.get_type_of_brake_display()

    class Meta:
        model = Brake
        read_only_fields = ["id"]
        exclude = list(set(
            RZWheelWZAxleBrakeAllSerializer.Meta.exclude + OtherWheelAxleBrakeAllSerializer.Meta.exclude
        ) - {"rigging_spring_force"})


class BrakeListSerializer(CustomModelSerializer):
    """
    制动器列表 序列化器
    """
    type_of_brake = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()

    def get_type_of_brake(self, obj):
        return obj.brake_type.type_of_brake

    def get_label(self, obj):
        return "Brake"

    class Meta:
        model = Brake
        read_only_fields = ["id"]
        exclude = BrakePartSerializer.Meta.exclude


# 制动盘
class BrakeDiscTypeListSerializer(CustomModelSerializer):
    """
    制动盘(轮装/轴装)材料类型列表 序列化器
    """

    class Meta:
        model = BrakeDiscType
        read_only_fields = ["id"]
        exclude = ["is_deleted", "density_of_material", "modulus_of_elasticity", "poissons_ratio",
                   "max_allowed_puls_bending_stress", "coeff_of_thermal_expansion_alpha",
                   "coeff_of_thermal_conduction_at_0_c", "first_deriv_of_ctc_at_0_c",
                   "specific_heat_capacity_at_0_c", "first_deriv_of_the_shc_at_0_c",
                   "radiation_coeff_of_friction_surface", "radiation_coeff_of_cooling_surface"]


class BrakeDiscTypeSerializer(CustomModelSerializer):
    """
    制动盘材料类型 序列化器
    """

    class Meta:
        model = BrakeDiscType
        read_only_fields = ["id"]
        exclude = ["is_deleted"]


class BrakeDiscListSerializer(CustomModelSerializer):
    """
    制动盘列表 序列化器
    """
    label = serializers.SerializerMethodField()

    def get_label(self, obj):
        return "Brake Disc"

    class Meta:
        model = BrakeDisc
        read_only_fields = ["id"]
        exclude = ["is_deleted", "inner_diameter", "outer_diameter", "thickness_of_the_friction_ring", "free_convection",
                   "cooling_constant_cek", "cooling_constant_sigma", "reduction_of_convection_c1k", "number_of_ribs",
                   "thickness_of_the_ribs", "thickness_of_the_disc", "bf", "reib", "screw_envelope_outer_diameter"]


class WheelBrakeDiscAllSerializer(CustomModelSerializer):
    """
    轮装制动盘 序列化器
    BES3和超管可用
    """
    # main_type = serializers.SerializerMethodField()

    # def get_main_type(self, obj):
        # return obj.get_disc_type_display()

    class Meta:
        model = BrakeDisc
        read_only_fields = ["id"]
        exclude = ["is_deleted", "screw_envelope_outer_diameter"]


class AxleBrakeDiscAllSerializer(CustomModelSerializer):
    """
    轴装制动盘 序列化器
    BES3和超管可用
    """
    # main_type = serializers.SerializerMethodField()

    # def get_main_type(self, obj):
    #     return obj.get_disc_type_display()

    class Meta:
        model = BrakeDisc
        read_only_fields = ["id"]
        exclude = ["is_deleted"]


class BrakeDiscPartSerializer(CustomModelSerializer):
    """
    所有制动盘 序列化器
    可看字段最少的用户可用
    """

    class Meta:
        model = BrakeDisc
        read_only_fields = ["id"]
        exclude = BrakeDiscListSerializer.Meta.exclude


# 闸片闸瓦
class PadTypeListSerializer(CustomModelSerializer):
    """
    闸瓦/闸片材料类型列表 序列化器
    """

    class Meta:
        model = PadType
        read_only_fields = ["id"]
        exclude = ["is_deleted", "area_per_disc", "height_of_wear", "alpha_pad", "beta_pad", "gamma_pad",
                   "efficiency_of_disc"]


class PadTypeSerializer(CustomModelSerializer):
    """
    闸片/闸瓦材料类型增删改查 序列化器
    """

    class Meta:
        model = PadType
        read_only_fields = ["id"]
        exclude = ["is_deleted"]


class BrakeLiningShoeListSerializer(CustomModelSerializer):
    """
    闸片/闸瓦列表 序列化器
    """
    label = serializers.SerializerMethodField()

    def get_label(self, obj):
        return "Brake Pad"

    class Meta:
        model = BrakeLiningShoe
        read_only_fields = ["id"]
        exclude = ["is_deleted", "item_name", "alpha_pad", "pad_thickness", "pad_shape", "width", "length", "thickness",
                   "wearlimit"]


class BrakeLiningAllSerializer(CustomModelSerializer):
    """
    闸片 序列化器
    BES2和超管可用
    """
    # main_type = serializers.SerializerMethodField()

    # def get_main_type(self, obj):
    #     return obj.get_pad_type_display()

    class Meta:
        model = BrakeLiningShoe
        read_only_fields = ["id"]
        exclude = ["is_deleted", "width", "length", "thickness", "wearlimit"]


class BrakeShoeAllSerializer(CustomModelSerializer):
    """
    闸瓦 序列化器
    BES2和超管可用
    """
    # main_type = serializers.SerializerMethodField()

    # def get_main_type(self, obj):
    #     return obj.get_pad_type_display()

    class Meta:
        model = BrakeLiningShoe
        read_only_fields = ["id"]
        exclude = ["is_deleted", "item_name", "alpha_pad", "pad_thickness", "pad_shape"]


class BrakeLiningShoePartSerializer(CustomModelSerializer):
    """
    闸片/闸瓦 序列号器
    可看字段最少的用户可用
    """

    class Meta:
        model = BrakeLiningShoe
        read_only_fields = ["id"]
        exclude = list(set(BrakeLiningAllSerializer.Meta.exclude + BrakeShoeAllSerializer.Meta.exclude))


# 调整阀
class ValveListSerializer(CustomModelSerializer):
    """
    调整阀列表 序列化器
    """
    label = serializers.SerializerMethodField()

    def get_label(self, obj):
        return "Valve"

    class Meta:
        model = Valve
        read_only_fields = ["id"]
        exclude = ["is_deleted", "c_0_high", "c_100_high", "aw_0", "aw_100", "c_apply", "t_0", "t_100", "c_max",
                   "factor_f2p", "f_apply", "rv_factor", "high_low", "c_max_nb", "edu_offset", "a_0_high", "a_100_high",
                   "cv_max_sb", "v_switch_h_l", "c_0_low", "c_100_low", "a_0_low", "a_100_low"]


class RVValveSerializer(CustomModelSerializer):
    """
    RV调整阀 序列化器
    """
    # main_type = serializers.SerializerMethodField()

    # def get_main_type(self, obj):
    #     return obj.get_mode_display()

    class Meta:
        model = Valve
        read_only_fields = ["id"]
        exclude = ["is_deleted", "high_low",  "c_max_nb", "edu_offset", "a_0_high", "a_100_high", "cv_max_sb",
                   "v_switch_h_l", "c_0_low", "c_100_low", "a_0_low", "a_100_low"]


class EDUValveSerializer(CustomModelSerializer):
    """
    EDU(BDV)-High/Low为False的调整阀 序列化器
    """
    # main_type = serializers.SerializerMethodField()

    # def get_main_type(self, obj):
    #     return obj.get_mode_display()

    class Meta:
        model = Valve
        read_only_fields = ["id"]
        exclude = ["is_deleted", "c_max", "factor_f2p", "f_apply", "rv_factor", "v_switch_h_l", "c_0_low", "c_100_low",
                   "a_0_low", "a_100_low"]


class EDUHLValveSerializer(CustomModelSerializer):
    """
    EDU(BDV)-High/Low为True的调整阀 序列化器
    """
    # main_type = serializers.SerializerMethodField()

    # def get_main_type(self, obj):
    #     return obj.get_mode_display()

    class Meta:
        model = Valve
        read_only_fields = ["id"]
        exclude = ["is_deleted", "c_max", "factor_f2p", "f_apply", "rv_factor"]


# MTB
class MTBListSerializer(CustomModelSerializer):
    """
    MTB列表 序列化器
    """
    label = serializers.SerializerMethodField()

    def get_label(self, obj):
        return "MTB"

    class Meta:
        model = MTB
        read_only_fields = ["id"]
        exclude = ["is_deleted", "v_max", "step", "v_off", "total_actractive_force", "efficiency", "curve_data"]


class MTBSerializer(CustomModelSerializer):
    """
    MTB 序列化器
    """
    # main_type = serializers.SerializerMethodField()

    # def get_main_type(self, obj):
    #     return obj.get_mtb_type_display()

    class Meta:
        model = MTB
        read_only_fields = ["id"]
        exclude = ["is_deleted"]


UNIT_DICT = {
    "Basic Element": BasicElementSerializer,
    "Car": CarSerializer,
    "Brake": BrakeListSerializer,
    "Brake Disc": BrakeDiscListSerializer,
    "Brake Pad": BrakeLiningShoeListSerializer,
    "Valve": ValveListSerializer,
    "MTB": MTBListSerializer
}

ALL_FIELDS_DICT = {
    "Brake": BrakeListSerializer.Meta.exclude,
    "BrakeDisc": BrakeDiscListSerializer.Meta.exclude,
    "BrakeLiningShoe": BrakeLiningShoeListSerializer.Meta.exclude,
    "Valve": ValveListSerializer.Meta.exclude,
    "MTB": MTBListSerializer.Meta.exclude
}

MAIN_TYPE_FUNC_DICT = {
    "Brake": lambda x, y: x.objects.get(pk=y.unit).brake_type.get_type_of_brake_display(),
    "BrakeDisc": lambda x, y: x.objects.get(pk=y.unit).get_type_of_disc_display(),
    "BrakeLiningShoe": lambda x, y: x.objects.get(pk=y.unit).get_type_of_pad_display(),
    "Valve": lambda x, y: x.objects.get(pk=y.unit).get_mode_display(),
    "MTB": lambda x, y: x.objects.get(pk=y.unit).get_mtb_type_display(),
}


# 部件管理
class CommonManagementListSerializer(CustomModelSerializer):
    """
    公用的部件管理 序列化器
    """
    is_check = serializers.SerializerMethodField()

    def get_is_check(self, obj):
        qs = UnitCheck.objects.filter(unit=obj.pk)
        return True if (qs and qs.first().state == 1) else False


class BrakeManagementListSerializer(CommonManagementListSerializer):
    """
    制动器管理列表 序列化器
    """

    class Meta:
        model = Brake
        read_only_fields = ["id"]
        exclude = BrakeListSerializer.Meta.exclude


class BrakeDiscManagementListSerializer(CommonManagementListSerializer):
    """
    制动盘管理列表 序列化器
    """

    class Meta:
        model = BrakeDisc
        read_only_fields = ["id"]
        exclude = BrakeDiscListSerializer.Meta.exclude


class BrakePadManagementListSerializer(CommonManagementListSerializer):
    """
    闸片闸瓦管理列表 序列化器
    """

    class Meta:
        model = BrakeLiningShoe
        read_only_fields = ["id"]
        exclude = BrakeLiningShoeListSerializer.Meta.exclude


class ValveManagementListSerializer(CommonManagementListSerializer):
    """
    调整阀管理列表 序列化器
    """

    class Meta:
        model = Valve
        read_only_fields = ["id"]
        exclude = ValveListSerializer.Meta.exclude


class MTBManagementListSerializer(CommonManagementListSerializer):
    """
    MTB管理列表 序列化器
    """

    class Meta:
        model = MTB
        read_only_fields = ["id"]
        exclude = MTBListSerializer.Meta.exclude


# 部件审核
class UnitCheckSerializer(CustomModelSerializer):
    """
    部件审核增删改查 序列化器
    """
    unit_class_name = serializers.SerializerMethodField()
    unit_name = serializers.SerializerMethodField()
    checker_name = serializers.SerializerMethodField()
    checker_role = serializers.SerializerMethodField()
    main_type = serializers.SerializerMethodField()
    img = serializers.SerializerMethodField()

    def get_unit_class_name(self, obj):
        return obj.get_unit_class_display()

    def get_unit_name(self, obj):
        return globals()[obj.get_unit_class_display()].objects.get(pk=obj.unit).item

    def get_checker_name(self, obj):
        return obj.checker.username

    def get_checker_role(self, obj):
        return obj.checker.role.all().values_list('name', flat=True)

    def get_main_type(self, obj):
        model_name = obj.get_unit_class_display()
        model = globals()[model_name]
        return MAIN_TYPE_FUNC_DICT[model_name](model, obj)

    def get_img(self, obj):
        return globals()[obj.get_unit_class_display()].objects.get(pk=obj.unit).img

    class Meta:
        model = UnitCheck
        read_only_fields = ["id"]
        exclude = ["is_deleted"]


# 部件类型管理（制动盘类型 | 闸片闸瓦类型）
class BrakeDiscTypeListManagementSerializer(CustomModelSerializer):
    """
    制动盘类型管理列表 序列化器
    """

    class Meta:
        model = BrakeDiscType
        read_only_fields = ["id"]
        exclude = ["is_deleted", "density_of_material", "modulus_of_elasticity", "poissons_ratio",
                   "max_allowed_puls_bending_stress", "coeff_of_thermal_expansion_alpha",
                   "coeff_of_thermal_conduction_at_0_c", "first_deriv_of_ctc_at_0_c", "specific_heat_capacity_at_0_c",
                   "first_deriv_of_the_shc_at_0_c", "radiation_coeff_of_friction_surface",
                   "radiation_coeff_of_cooling_surface"]


class BrakeDiscTypePostManagementSerializer(CustomModelSerializer):
    """
    制动盘类型管理增 序列化器
    """

    class Meta:
        model = BrakeDiscType
        read_only_fields = ["id"]
        exclude = ["is_deleted"]


class BrakeDiscTypeUpdateManagementSerializer(CustomModelSerializer):
    """
    闸片闸瓦类型管理增删改 序列化器
    """

    class Meta:
        model = BrakeDiscType
        read_only_fields = ["id"]
        exclude = ["is_deleted", "name"]


class PadTypeListManagementSerializer(CustomModelSerializer):
    """
    闸片闸瓦类型管理列表 序列化器
    """

    class Meta:
        model = PadType
        read_only_fields = ["id"]
        exclude = ["is_deleted", "area_per_disc", "height_of_wear", "alpha_pad", "beta_pad", "gamma_pad",
                   "efficiency_of_disc"]


class PadTypePostManagementSerializer(CustomModelSerializer):
    """
    闸片闸瓦类型管理增 序列化器
    """

    class Meta:
        model = PadType
        read_only_fields = ["id"]
        exclude = ["is_deleted"]


class PadTypeUpdateManagementSerializer(CustomModelSerializer):
    """
    闸片闸瓦类型管理增删改 序列化器
    """

    class Meta:
        model = PadType
        read_only_fields = ["id"]
        exclude = ["is_deleted", "name"]
