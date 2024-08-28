import math
from dataclasses import dataclass
from project.models import *
from project.views.calculation.dataclass import *
from project.views.calculation.inerface import *
from project.views.calculation.service.build_calculation_system import *
from project.views.calculation.service.generate_calculator import *
from project.views.calculation.utils import *



@dataclass
class OneStepSetttings(Component):
    oneStepInputs: dict

    def __post_init__(self):
        try:
            inputs = self.oneStepInputs["oneStep"]
            self.wheelSettingMode = inputs["wheelSettingMode"]
            self.verticalMove = float(inputs["verticalMove"])
            self.lateralMove = float(inputs["lateralMove"])
            self.longMove = float(inputs["longMove"])
            self.padWear = float(inputs["padWear"])
            self.discWear = float(inputs["discWear"])
            self.fPointOffset = float(inputs["fPointOffset"])
            self.brakingApplied = inputs["brakingApplied"]
            self.padHolderBoltWear = float(inputs["padHolderBoltWear"])
            self.leverBoltWear = float(inputs["leverBoltWear"])

        except KeyError as e:
            print(f"Missing key in form data: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

class OneStepCalculation(BXCalculationModeBase):
    def __init__(self,bxCalculationSystem:BXCalculationSystem) -> None:
        super().__init__()
        self.bxCalculationSystem=bxCalculationSystem
        self.mode_inputs=OneStepSetttings(self.bxCalculationSystem.bogie_brake_system.functionalInputs.inputs)

    def calculation_results(self):

        """ 
            Basic Inputs for Static Positioning and Dynamic 
        """

        "static position"
        E_dimension = self.bxCalculationSystem.bogie_brake_system.brakeCaliperPositioning.eDimension
        angle = self.bxCalculationSystem.bogie_brake_system.brakeCaliperPositioning.rotationOfCaliper
        z_offset = self.bxCalculationSystem.bogie_brake_system.brakeCaliperPositioning.installationOffsetZ
        y_offset = self.bxCalculationSystem.bogie_brake_system.brakeCaliperPositioning.installationOffsetY
        clearance = self.bxCalculationSystem.bogie_brake_system.pad.clearance

        "dynamic movement"
        'movement'
        x_move= self.bxCalculationSystem.bogie_brake_system.kinematicPrimarySuspension.X_LongitudinalMovement
        y_move = self.bxCalculationSystem.bogie_brake_system.kinematicPrimarySuspension.Y_LateralMovement
        'wear'
        disc_wear = self.bxCalculationSystem.bogie_brake_system.brakeCaliperPositioning.discWear
        pad_wear = self.bxCalculationSystem.bogie_brake_system.brakeCaliperPositioning.padWear

        "disc selection"
        disc_inner=self.bxCalculationSystem.bogie_brake_system.disc.discInnerDiameter
        disc_outer = self.bxCalculationSystem.bogie_brake_system.disc.discOuterDiameter
        Disc_Width = self.bxCalculationSystem.bogie_brake_system.disc.discWidth

        "pad selection"
        Pad_thickness = self.bxCalculationSystem.bogie_brake_system.pad.padThickness
        shape_data=self.bxCalculationSystem.pad_shape


        """ 
            Specific Settings and offsets calculation due to caliper movement/wear
        """

        "on setp setting with movement and wear"
        f_point_offset= self.mode_inputs.fPointOffset
        x_move_instant= self.mode_inputs.longMove
        y_move_instant= self.mode_inputs.lateralMove
        z_move_instant= self.mode_inputs.verticalMove
        pad_wear_instant= self.mode_inputs.padWear
        disc_wear_instant= self.mode_inputs.discWear
        PHBW_instant= self.mode_inputs.padHolderBoltWear
        LBW_instant= self.mode_inputs.leverBoltWear

        "offset due to caliper movement/wear"
        instantdata=self.bxCalculationSystem.actuator_calculator.transfer_list_instant( 
            y_move_instant=y_move_instant, disc_wear_instant=disc_wear_instant, pad_wear_instant=pad_wear_instant, WLB_instant=LBW_instant, WPHB_instant=PHBW_instant
            )
        D_w_l_Instant=instantdata.D_w_l_Instant
        Delta_Z_Instant=instantdata.Delta_Z_Instant
        Delta_Z = instantdata.Delta_Z

        """
        Calculation for this mode
        """

        "Inital position calculation"
        F_point=self.bxCalculationSystem.F_point
        E=E_dimension-f_point_offset
        F_offset=E-F_point
        fix_x=F_offset
        angle = angle * math.pi / 180

        points_group=[]
        n_area=int(shape_data[0][3])
        shape_data_list=[[] for i in range(n_area)]
        base_initial = [[] for i in range(n_area)]
        initial_group = [[] for i in range(n_area)]
        n_lower=4+n_area

        for i in range(0, n_area):
            n_points=int(shape_data[0][4+i])
            points_group.append(n_points)
            for j in range(0,n_points):
                shape_data_list[i].append([shape_data[0][j+n_lower]+fix_x, shape_data[1][j+n_lower]])
                shape_x0 = shape_data[0][j + n_lower] + fix_x
                shape_y0 = shape_data[1][j + n_lower]
                shape_x = shape_x0 * math.cos(angle) + (shape_y0 + Delta_Z) * math.sin(angle)
                shape_y = -1 * shape_x0 * math.sin(angle) + (shape_y0 + Delta_Z) * math.cos(angle)
                base_initial[i].append([shape_x, shape_y])
            n_lower=n_lower+n_points

        "Friction Radius of this step"
        E_delta_Rm = D_w_l_Instant - (z_offset + z_move_instant) * math.sin(angle) + x_move_instant * math.cos(angle)
        V_Rm = (z_offset + z_move_instant) * math.cos(angle) + x_move_instant * math.sin(angle) + Delta_Z_Instant
        R_m=EclipseCalculationUtils.Rm_cal(points_group, shape_data_list, E_dimension, E_delta_Rm, V_Rm)
        # R_m=Rm_cal(points_group, shape_data_list, E_dimension, E_delta_Rm, V_Rm)
            
        "Final Position of this step"
        n_area = len(points_group)
        for i in range(0,n_area):
            n_points = points_group[i]
            for j in range(0, n_points):
                shape_x = base_initial[i][j][0]+D_w_l_Instant*math.cos(angle)+Delta_Z_Instant* math.sin(angle)+x_move_instant
                shape_y = base_initial[i][j][1]-D_w_l_Instant * math.sin(angle)+Delta_Z_Instant *math.cos(angle)+z_offset+z_move_instant
                initial_group[i].append([shape_x,shape_y])

        "Extreme inner and outter points"
        initial_innermost =EclipseCalculationUtils.innermost(initial_group)
        initial_outermost =EclipseCalculationUtils.outermost(initial_group)

        "Circles of disc and friction radius of this step"
        circle_outer = EclipseCalculationUtils.circle_array(disc_outer)
        circle_inner = EclipseCalculationUtils.circle_array(disc_inner)
        circle_rm=EclipseCalculationUtils.circle_array(R_m*2)

        "Calculation Outputs"
        inner_outer_points={
                            "initial_innermost":initial_innermost,"initial_outermost": initial_outermost,
                            }
        
        data_group={
                    "very_original_shape_data":shape_data_list,
                    "n_area":n_area,
                    "points_group":points_group,
                    "initial_group":initial_group,
                    "circle_outer":circle_outer,
                    "circle_inner":circle_inner,
                    "R_m":R_m,
                    "circle_rm":circle_rm,
                    "inner_outer_points":inner_outer_points,
                    "E_delta_Rm": [E_delta_Rm,V_Rm,x_move_instant,math.cos(angle),z_offset,z_move_instant,math.sin(angle)]
                    }

        return data_group
