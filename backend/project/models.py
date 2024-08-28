from django.db import models

from dvadmin.utils.models import CoreModel, table_prefix
from dvadmin.system.models import Users, Role, Dept

# Create your models here.

class Car(CoreModel):
    CAR_TYPE_CHOICES = (
        (0, "Motor Car"),
        (1, "Trailer Car")
    )
    car_type = models.SmallIntegerField(choices=CAR_TYPE_CHOICES, blank=False, verbose_name="车辆类型", help_text="车辆类型")
    name = models.CharField(max_length=255, blank=False, verbose_name="车辆名称", help_text="车辆名称")
    img = models.CharField(max_length=255, blank=False, verbose_name="图片路径", help_text="图片路径")
    detail = models.JSONField(default=dict, blank=True, verbose_name="详情", help_text="详情")
    is_global = models.BooleanField(default=1, blank=True, verbose_name="是否全局", help_text="是否全局")

    class Meta:
        db_table = table_prefix + "project_car"
        verbose_name = "车辆表"
        verbose_name_plural = verbose_name

class BasicElement(CoreModel):
    name = models.CharField(max_length=255, blank=False, verbose_name="基础部件名称", help_text="基础部件名称")
    img = models.CharField(max_length=255, blank=False, verbose_name="图片路径", help_text="图片路径")
    detail = models.JSONField(default=dict, blank=True, verbose_name="详情", help_text="详情")
    is_global = models.BooleanField(default=1, blank=True, verbose_name="是否全局", help_text="是否全局")

    class Meta:
        db_table = table_prefix + "project_basic_element"
        verbose_name = "基础部件表"
        verbose_name_plural = verbose_name



class BrakeType(CoreModel):
    name = models.CharField(max_length=255, blank=False, verbose_name="类型名称", help_text="类型名称")
    BRAKE_TYPE_CHOICES = (
        (0, "Wheelact"),
        (1, "Axleact"),
        (2, "Treadact")
    )
    type_of_brake = models.SmallIntegerField(choices=BRAKE_TYPE_CHOICES, blank=False, verbose_name="制动器类别")

    class Meta:
        db_table = table_prefix + "project_brake_type"
        verbose_name = "制动器类型表"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


class Brake(CoreModel):

    # MSE只能查看的字段，BES2可查看的字段，踏面Treadact，轮装Wheelact和轴装Axleact公共字段
    brake_type = models.ForeignKey(to=BrakeType, on_delete=models.CASCADE, db_constraint=False, blank=False,
                                   verbose_name="制动器类型", help_text="制动器类型")
    item = models.CharField(max_length=255, blank=False, verbose_name="Item", help_text="Item")
    img = models.CharField(max_length=255, blank=False, verbose_name="图片路径", help_text="图片路径")
    is_global = models.BooleanField(default=0, blank=True, verbose_name="是否全局", help_text="是否全局")
    # is_check = models.BooleanField(default=0, blank=True, verbose_name="审核状态", help_text="审核状态")
    cylinder_area = models.FloatField(default=0, blank=True, verbose_name="Cylinder Area", help_text="Cylinder Area")
    cylinder_efficiency = models.FloatField(default=0, blank=True, verbose_name="Cylinder Efficiency",
                                            help_text="Cylinder Efficiency")
    cylinder_ratio = models.FloatField(default=0, blank=True, verbose_name="Cylinder Ratio", help_text="Cylinder Ratio")
    cylinder_spring_force = models.FloatField(default=0, blank=True, verbose_name="Cylinder Spring Force",
                                              help_text="Cylinder Spring Force")
    rigging_efficiency = models.FloatField(default=0, blank=True, verbose_name="Riggign Efficiency",
                                           help_text="Riggign Efficiency")
    rigging_ratio = models.FloatField(default=0, blank=True, verbose_name="Rigging Ratio", help_text="Rigging Ratio")
    transmission_efficiency = models.FloatField(default=0, blank=True, verbose_name="Transmission Efficiency",
                                                help_text="Transmission Efficiency")
    transmission_ratio = models.FloatField(default=0, blank=True, verbose_name="Transmission Ratio",
                                           help_text="Transmission Ratio")
    brake_pad_area = models.FloatField(default=0, blank=True, verbose_name="Brake Pad Area", help_text="Brake Pad Area")
    number_of_pad_per_brake_cylinder = models.FloatField(default=0, blank=True,
                                                         verbose_name="Number Of Pad Per Brake Cylinder",
                                                         help_text="Number Of Pad Per Brake Cylinder")
    friction_area_of_the_disc = models.FloatField(default=0, blank=True, verbose_name="Friction Area Of The Disc",
                                                  help_text="Friction Area Of The Disc")
    pressure_limit = models.FloatField(default=0, blank=True, verbose_name="Pressure Limit", help_text="Pressure Limit")
    pb_force = models.FloatField(default=0, blank=True, verbose_name="PB Force", help_text="PB Force")

    # 踏面附加字段，只有MSE能看
    rigging_spring_force = models.FloatField(default=0, blank=True, verbose_name="rigging_spring_force",
                                             help_text="rigging_spring_force")

    # BES2可查看的字段，轮装Wheelact的RZ类型和轴装Axleact的WZ类型共有的字段
    lever_length = models.FloatField(default=0, blank=True, verbose_name="Lever Length", help_text="Lever Length")
    lever_length_the_front = models.FloatField(default=0, blank=True, verbose_name="Lever Length The Frone",
                                               help_text="Lever Length The Frone")
    offset_pull_rod_rotation_point_in_lever = models.FloatField(default=0, blank=True,
                                                                verbose_name="Offset Pull Rod Rotation Point In Lever",
                                                                help_text="Offset Pull Rod Rotation Point In Lever")
    pad_holder_height = models.FloatField(default=0, blank=True, verbose_name="Pad Holder Height",
                                          help_text="Pad Holder Height")
    wear_of_lever_bolt = models.FloatField(default=0, blank=True, verbose_name="Wear Of Lever Bolt",
                                           help_text="Wear Of Lever Bolt")
    wear_of_pad_holder_bolt = models.FloatField(default=0, blank=True, verbose_name="Wear Of Pad Holder Bolt",
                                                help_text="Wear Of Pad Holder Bolt")
    distance_cylinder_fixation_yoke_fixation = models.FloatField(
        default=0, blank=True,
        verbose_name="Distance Cylinder Fixation Yoke Fixation",
        help_text="Distance Cylinder Fixation Yoke Fixation"
    )
    pre_adjustment_in_cylinder = models.FloatField(default=0, blank=True, verbose_name="Pre Adjustment In Cylinder",
                                                   help_text="Pre Adjustment In Cylinder")
    gdimension = models.FloatField(default=0, blank=True, verbose_name="Gdimension", help_text="Gdimension")
    hanger_upper_bolt_to_lower_bolt = models.FloatField(default=0, blank=True,
                                                        verbose_name="Hanger Upper Bolt To Lower Bolt",
                                                        help_text="Hanger Upper Bolt To Lower Bolt")
    hanger_lower_bolt_to_pad_holder_assemble_surface = models.FloatField(
                                                        default=0, blank=True,
                                                        verbose_name="Hanger Lower Bolt To Pad Holder Assemble Surface",
                                                        help_text="Hanger Lower Bolt To Pad Holder Assemble Surface")
    dis_between_hanger_upper_bolt = models.FloatField(
        default=0, blank=True, verbose_name="Dis Between Hanger Upper Bolt", help_text="Dis Between Hanger Upper Bolt"
    )
    hanger_upper_bolt_to_caliper_center = models.FloatField(default=0, blank=True,
                                                            verbose_name="Hanger Upper Bolt To Caliper Center",
                                                            help_text="Hanger Upper Bolt To Caliper Center")
    hanger_lower_bolt_to_pad_center = models.FloatField(default=0, blank=True,
                                                        verbose_name="Hanger Lower Bolt To Pad Center",
                                                        help_text="Hanger Lower Bolt To Pad Center")

    # BES2可查看的字段，轮装Wheelact和轴装Axleact的其他类型共有的字段，踏面Thread没有的字段
    ll = models.FloatField(default=0, blank=True, verbose_name="LL", help_text="LL")
    lr = models.FloatField(default=0, blank=True, verbose_name="LR", help_text="LR")
    lr1 = models.FloatField(default=0, blank=True, verbose_name="LR1", help_text="LR1")
    lr2 = models.FloatField(default=0, blank=True, verbose_name="LR2", help_text="LR2")
    d1 = models.FloatField(default=0, blank=True, verbose_name="D1", help_text="D1")
    d2 = models.FloatField(default=0, blank=True, verbose_name="D2", help_text="D2")
    d3 = models.FloatField(default=0, blank=True, verbose_name="D3", help_text="D3")
    h1 = models.FloatField(default=0, blank=True, verbose_name="H1", help_text="H1")
    h2 = models.FloatField(default=0, blank=True, verbose_name="H2", help_text="H2")
    h3 = models.FloatField(default=0, blank=True, verbose_name="H3", help_text="H3")
    h4 = models.FloatField(default=0, blank=True, verbose_name="H4", help_text="H4")

    class Meta:
        db_table = table_prefix + "project_brake"
        verbose_name = "制动器表"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


class BrakeDiscType(CoreModel):
    # material材料
    name = models.CharField(max_length=255, blank=False, verbose_name="类型材料", help_text="类型材料")
    density_of_material = models.FloatField(default=0, blank=True, verbose_name="density_of_material",
                                            help_text="density_of_material")
    modulus_of_elasticity = models.FloatField(default=0, blank=True, verbose_name="modulus_of_elasticity",
                                              help_text="modulus_of_elasticity")
    poissons_ratio = models.FloatField(default=0, blank=True, verbose_name="poissons_ratio", help_text="poissons_ratio")
    max_allowed_puls_bending_stress = models.FloatField(default=0, blank=True,
                                                        verbose_name="max_allowed_puls_bending_stress",
                                                        help_text="max_allowed_puls_bending_stress")
    coeff_of_thermal_expansion_alpha = models.FloatField(default=0, blank=True,
                                                         verbose_name="coeff_of_thermal_expansion_alpha",
                                                         help_text="coeff_of_thermal_expansion_alpha")
    coeff_of_thermal_conduction_at_0_c = models.FloatField(default=0, blank=True,
                                                           verbose_name="coeff_of_thermal_conduction_at_0_c",
                                                           help_text="coeff_of_thermal_conduction_at_0_c")
    first_deriv_of_ctc_at_0_c = models.FloatField(default=0, blank=True, verbose_name="first_deriv_of_ctc_at_0_c",
                                                  help_text="first_deriv_of_ctc_at_0_c")
    specific_heat_capacity_at_0_c = models.FloatField(
        default=0, blank=True, verbose_name="specific_heat_capacity_at_0_c", help_text="specific_heat_capacity_at_0_c"
    )
    first_deriv_of_the_shc_at_0_c = models.FloatField(
        default=0, blank=True, verbose_name="first_deriv_of_the_shc_at_0_c", help_text="first_deriv_of_the_shc_at_0_c"
    )
    radiation_coeff_of_friction_surface = models.FloatField(default=0, blank=True,
                                                            verbose_name="radiation_coeff_of_friction_surface",
                                                            help_text="radiation_coeff_of_friction_surface")
    radiation_coeff_of_cooling_surface = models.FloatField(default=0, blank=True,
                                                           verbose_name="radiation_coeff_of_cooling_surface",
                                                           help_text="radiation_coeff_of_cooling_surface")

    class Meta:
        db_table = table_prefix + "project_brake_disc_type"
        verbose_name = "制动盘类型表"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


class BrakeDisc(CoreModel):

    # BES3只能查看的字段
    disc_type = models.ForeignKey(to=BrakeDiscType, on_delete=models.CASCADE, db_constraint=False, blank=False,
                                  verbose_name="制动盘类型", help_text="制动盘类型")
    DISC_TYPE_CHOICES = (
        (0, "Wheelact"),
        (1, "Axleact")
    )
    type_of_disc = models.SmallIntegerField(choices=DISC_TYPE_CHOICES, blank=False, verbose_name="制动盘类别",
                                            help_text="制动盘类别")
    item = models.CharField(max_length=255, blank=False, verbose_name="Item", help_text="Item")
    img = models.CharField(max_length=255, blank=False, verbose_name="图片路径", help_text="图片路径")
    is_global = models.BooleanField(default=0, blank=True, verbose_name="是否全局", help_text="是否全局")

    # 公共字段
    inner_diameter = models.FloatField(default=0, blank=True, verbose_name="inner_diameter", help_text="inner_diameter")
    outer_diameter = models.FloatField(default=0, blank=True, verbose_name="outer_diameter", help_text="outer_diameter")
    thickness_of_the_friction_ring = models.FloatField(default=0, blank=True,
                                                       verbose_name="thickness_of_the_friction_ring",
                                                       help_text="thickness_of_the_friction_ring")
    free_convection = models.FloatField(default=0, blank=True, verbose_name="free_convection",
                                        help_text="free_convection")
    cooling_constant_cek = models.FloatField(default=0, blank=True, verbose_name="cooling_constant_cek",
                                             help_text="cooling_constant_cek")
    cooling_constant_sigma = models.FloatField(default=0, blank=True, verbose_name="cooling_constant_sigma",
                                               help_text="cooling_constant_sigma")
    reduction_of_convection_c1k = models.FloatField(default=0, blank=True, verbose_name="reduction_of_convection_c1k",
                                                    help_text="reduction_of_convection_c1k")
    number_of_ribs = models.FloatField(default=0, blank=True, verbose_name="number_of_ribs", help_text="number_of_ribs")
    thickness_of_the_ribs = models.FloatField(default=0, blank=True, verbose_name="thickness_of_the_ribs",
                                              help_text="thickness_of_the_ribs")
    thickness_of_the_disc = models.FloatField(default=0, blank=True, verbose_name="thickness_of_the_disc",
                                              help_text="thickness_of_the_disc")
    bf = models.FloatField(default=0, blank=True, verbose_name="BF", help_text="BF")
    reib = models.FloatField(default=0, blank=True, verbose_name="REIB", help_text="REIB")

    # 轴装制动盘附加字段
    screw_envelope_outer_diameter = models.FloatField(
        default=0, blank=True, verbose_name="screw_envelope_outer_diameter", help_text="screw_envelope_outer_diameter"
    )

    class Meta:
        db_table = table_prefix + "project_brake_disc"
        verbose_name = "制动盘表"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


class PadType(CoreModel):
    # material材料
    name = models.CharField(max_length=255, blank=False, verbose_name="类型材料", help_text="类型材料")
    area_per_disc = models.FloatField(default=0, verbose_name="area_per_disc", help_text="area_per_disc")
    height_of_wear = models.FloatField(default=0, verbose_name="height_of_wear", help_text="height_of_wear")
    alpha_pad = models.FloatField(default=0, verbose_name="alpha_pad", help_text="alpha_pad")
    beta_pad = models.FloatField(default=0, verbose_name="beta_pad", help_text="beta_pad")
    gamma_pad = models.FloatField(default=0, verbose_name="gamma_pad", help_text="gamma_pad")
    efficiency_of_disc = models.FloatField(default=0, verbose_name="efficiency_of_disc", help_text="efficiency_of_disc")

    class Meta:
        db_table = table_prefix + "project_pad_type"
        verbose_name = "闸片闸瓦类型表"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


class BrakeLiningShoe(CoreModel):

    # 闸片闸瓦公共字段
    pad_type = models.ForeignKey(to=PadType, on_delete=models.CASCADE, db_constraint=False, blank=False,
                                 verbose_name="闸片/闸瓦类别", help_text="闸片/闸瓦类别")
    PAD_TYPE_CHOICES = (
        (0, "Brake Lining"),
        (1, "Brake Shoe")
    )
    type_of_pad = models.SmallIntegerField(choices=PAD_TYPE_CHOICES, blank=False, verbose_name="类型", help_text="类型")
    item = models.CharField(max_length=255, blank=False, verbose_name="Item", help_text="Item")
    img = models.CharField(max_length=255, blank=False, verbose_name="图片路径", help_text="图片路径")
    is_global = models.BooleanField(default=0, blank=True, verbose_name="是否全局", help_text="是否全局")

    # 闸片专用字段
    item_name = models.CharField(max_length=255, blank=True, verbose_name="Item Name", help_text="Item Name")
    alpha_pad = models.FloatField(default=0, blank=True, verbose_name="alpha_pad", help_text="alpha_pad")
    pad_thickness = models.FloatField(default=0, blank=True, verbose_name="pad_thickness", help_text="pad_thickness")
    pad_shape = models.JSONField(default=dict, blank=True, verbose_name="详情", help_text="详情")

    # 闸瓦专用字段
    width = models.FloatField(default=0, blank=True, verbose_name="width", help_text="width")
    length = models.FloatField(default=0, blank=True, verbose_name="length", help_text="length")
    thickness = models.FloatField(default=0, blank=True, verbose_name="thickness", help_text="thickness")
    wearlimit = models.FloatField(default=0, blank=True, verbose_name="wearlimit", help_text="wearlimit")

    class Meta:
        db_table = table_prefix + "project_brake_lining_shoe"
        verbose_name = "闸片闸瓦表"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


class Valve(CoreModel):

    item = models.CharField(max_length=255, blank=False, verbose_name="调整阀名称", help_text="调整阀名称")
    img = models.CharField(max_length=255, blank=False, verbose_name="图片路径", help_text="图片路径")
    is_global = models.BooleanField(default=0, blank=True, verbose_name="是否全局", help_text="是否全局")
    MODE = (
        (0, "RV"),
        (1, "EDU")
    )
    mode = models.SmallIntegerField(choices=MODE, blank=False, verbose_name="调整阀类型", help_text="调整阀类型")

    # 公共参数
    c_0_high = models.FloatField(default=0, blank=True, verbose_name="C_0_High", help_text="C_0_High")
    c_100_high = models.FloatField(default=0, blank=True, verbose_name="C_100_High", help_text="C_100_High")
    aw_0 = models.FloatField(default=0, blank=True, verbose_name="AW_0", help_text="AW_0")
    aw_100 = models.FloatField(default=0, blank=True, verbose_name="AW_100", help_text="AW_100")
    c_apply = models.FloatField(default=0, blank=True, verbose_name="C_Apply", help_text="C_Apply")
    t_0 = models.FloatField(default=0, blank=True, verbose_name="T_0", help_text="T_0")
    t_100 = models.FloatField(default=0, blank=True, verbose_name="T_100", help_text="T_100")

    # RV调整阀参数
    c_max = models.FloatField(default=0, blank=True, verbose_name="C_Max", help_text="C_Max")
    factor_f2p = models.FloatField(default=0, blank=True, verbose_name="Factor_F2P", help_text="Factor_F2P")
    f_apply = models.FloatField(default=0, blank=True, verbose_name="F_Apply", help_text="F_Apply")
    rv_factor = models.FloatField(default=0, blank=True, verbose_name="RV_Factor", help_text="RV_Factor")

    # EDU调整阀参数
    high_low = models.BooleanField(default=False, blank=True, verbose_name="High/Low", help_text="High/Low")
    c_max_nb = models.FloatField(default=0, blank=True, verbose_name="C_Max_NB", help_text="C_Max_NB")
    edu_offset = models.FloatField(default=0, blank=True, verbose_name="EDU_Offset", help_text="EDU_Offset")
    a_0_high = models.FloatField(default=0, blank=True, verbose_name="A_0_High", help_text="A_0_High")
    a_100_high = models.FloatField(default=0, blank=True, verbose_name="A_100_High", help_text="A_100_High")
    cv_max_sb = models.FloatField(default=0, blank=True, verbose_name="Cv_Max_SB", help_text="Cv_Max_SB")

    # EDU的high_low为true的参数
    v_switch_h_l = models.FloatField(default=0, blank=True, verbose_name="V_Switch_H/L", help_text="V_Switch_H/L")
    c_0_low = models.FloatField(default=0, blank=True, verbose_name="C_0_Low", help_text="C_0_Low")
    c_100_low = models.FloatField(default=0, blank=True, verbose_name="C_100_Low", help_text="C_100_Low")
    a_0_low = models.FloatField(default=0, blank=True, verbose_name="A_0_Low", help_text="A_0_Low")
    a_100_low = models.FloatField(default=0, blank=True, verbose_name="A_100_Low", help_text="A_100_Low")

    class Meta:
        db_table = table_prefix + "project_valve"
        verbose_name = "调整阀表"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


class MTB(CoreModel):

    MTB_TYPE_CHOICES = (
        (0, "Rigid"),
        (1, "Articulated")
    )
    mtb_type = models.SmallIntegerField(choices=MTB_TYPE_CHOICES, blank=False, verbose_name="MTB类型", help_text="MTB类型")
    item = models.CharField(max_length=255, verbose_name="Item", help_text="Item")
    img = models.CharField(max_length=255, blank=False, verbose_name="图片路径", help_text="图片路径")
    is_global = models.BooleanField(default=0, blank=True, verbose_name="是否全局", help_text="是否全局")
    v_max = models.FloatField(default=0, verbose_name="V_Max(Km/h)", help_text="V_Max(Km/h)")
    step = models.FloatField(default=0, verbose_name="Step(Km/h)", help_text="Step(Km/h)")
    v_off = models.FloatField(default=0, verbose_name="V_Off(h/Km)", help_text="V_Off(h/Km)")
    total_actractive_force = models.FloatField(default=0, verbose_name="Total Actractive Force",
                                               help_text="Total Actractive Force")
    efficiency = models.FloatField(default=0, verbose_name="Efficiency", help_text="Efficiency")
    curve_data = models.JSONField(default=dict, blank=True, verbose_name="Cure Data", help_text="Cure Data")

    class Meta:
        db_table = table_prefix + "project_mtb"
        verbose_name = "磁轨制动器表"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


class UnitCheck(CoreModel):
    UNIT_CLASS = (
        (0, "Brake"),
        (1, "BrakeDisc"),
        (2, "BrakeLiningShoe"),
        (3, "Valve"),
        (4, "MTB")
    )
    unit_class = models.SmallIntegerField(choices=UNIT_CLASS, verbose_name="部件种类", help_text="部件种类")
    unit = models.BigIntegerField(verbose_name="审核部件", help_text="审核部件")
    checker = models.ForeignKey(to=Users, on_delete=models.CASCADE, db_constraint=False, blank=True,
                                verbose_name="审核人", help_text="审核人", related_name="unit_checker")
    # 0未审核，1通过，2拒绝
    state = models.SmallIntegerField(default=0, blank=True, verbose_name="审核状态", help_text="审核状态")

    class Meta:
        db_table = table_prefix + "project_unit_check"
        verbose_name = "部件审核表"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)

