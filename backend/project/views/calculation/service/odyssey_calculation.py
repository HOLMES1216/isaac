import math
from dataclasses import dataclass
from project.models import *
from functools import cached_property
import time
import numpy as np
from project.views.calculation.dataclass import *
from project.views.calculation.inerface import *
from project.views.calculation.service.build_calculation_system import *
from project.views.calculation.service.generate_calculator import *
from project.views.calculation.utils import *



@dataclass
class OdysseySetttings(Component):
    odysseyInputs: dict

    def __post_init__(self):
        try:
            inputs = self.odysseyInputs["odyssey"]
            """ must ask frontend add this data field !!!"""
            self.wheelInnerCheck = True
        except KeyError as e:
            print(f"Missing key in form data: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

class OdysseyCalculation(BXCalculationModeBase):
    def __init__(self,bxCalculationSystem:BXCalculationSystem) -> None:
        super().__init__()
        self.bxCalculationSystem=bxCalculationSystem
        self.mode_inputs=OdysseySetttings(self.bxCalculationSystem.bogie_brake_system.functionalInputs.inputs)

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
        lift_stop = self.bxCalculationSystem.bogie_brake_system.kinematicPrimarySuspension.A_TareDatumToLiftStop
        bump_stop = self.bxCalculationSystem.bogie_brake_system.kinematicPrimarySuspension.B_TareDatumToBumpStop
        crush = self.bxCalculationSystem.bogie_brake_system.kinematicPrimarySuspension.C_TareDatumToCrushDatum
        'wear'
        disc_wear = self.bxCalculationSystem.bogie_brake_system.brakeCaliperPositioning.discWear
        pad_wear = self.bxCalculationSystem.bogie_brake_system.brakeCaliperPositioning.padWear

        "disc selection"
        disc_inner=self.bxCalculationSystem.bogie_brake_system.disc.discInnerDiameter
        disc_outer = self.bxCalculationSystem.bogie_brake_system.disc.discOuterDiameter
        Disc_Width = self.bxCalculationSystem.bogie_brake_system.disc.discWidth
        wheel_screw = self.bxCalculationSystem.bogie_brake_system.wheel.wheelInnerDiameter
        "pad selection"
        Pad_thickness = self.bxCalculationSystem.bogie_brake_system.pad.padThickness
        shape_data=self.bxCalculationSystem.pad_shape

        """ 
            Specific Settings and offsets calculation due to caliper movement/wear
        """

        "offset due to caliper movement/wear"

        instantdata=self.bxCalculationSystem.actuator_calculator.transfer_list

        E_other = instantdata.E_other
        Delta_Z = instantdata.Delta_Z
        D_w_l_min_L0=instantdata.D_w_l_min_L0
        D_w_l_max_L0 = instantdata.D_w_l_max_L0
        D_w_l_min = instantdata.D_w_l_min
        D_w_l_max = instantdata.D_w_l_max
        Delta_Zmin=instantdata.Delta_Zmin
        Delta_Zmax = instantdata.Delta_Zmax

        """
        Calculation for this mode
        """

        "Inital position calculation"
        F_point=self.bxCalculationSystem.F_point
        E=E_dimension
        F_offset=E-F_point
        fix_x=F_offset
        angle = angle * math.pi / 180


        points_group=[]
        n_area=int(shape_data[0][3])
        shape_data_list=[[] for i in range(n_area)]
        base_initial = [[] for i in range(n_area)]
        initial_group = [[] for i in range(n_area)]
        tare_e_min_group = [[] for i in range(n_area)]
        tare_e_max_group = [[] for i in range(n_area)]
        crush_e_min_group = [[] for i in range(n_area)]
        crush_e_max_group = [[] for i in range(n_area)]
        wheel_inner_e_min_group = [[] for i in range(n_area)]
        wheel_inner_e_max_group = [[] for i in range(n_area)]
        lift_e_min_group = [[] for i in range(n_area)]
        lift_e_max_group = [[] for i in range(n_area)]
        bump_e_min_group = [[] for i in range(n_area)]
        bump_e_max_group = [[] for i in range(n_area)]
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

        "Friction Radius in initial state"
        R_m=EclipseCalculationUtils.Rm_cal(points_group, shape_data_list, E_dimension, 0, 0)
            
        "Generate different positions for multiple cases"
        n_area = len(points_group)
        for i in range(0,n_area):
            n_points = points_group[i]
            for j in range(0, n_points):

                shape_x=base_initial[i][j][0]
                shape_y=base_initial[i][j][1]+z_offset
                initial_group[i].append([shape_x,shape_y])

                shape_x = base_initial[i][j][0]+D_w_l_min_L0*math.cos(angle)
                shape_y = base_initial[i][j][1] + z_offset- D_w_l_min_L0 * math.sin(angle)
                tare_e_min_group[i].append([shape_x,shape_y])

                shape_x = base_initial[i][j][0]+D_w_l_max_L0*math.cos(angle)
                shape_y = base_initial[i][j][1] + z_offset- D_w_l_max_L0 * math.sin(angle)
                tare_e_max_group[i].append([shape_x,shape_y])

                shape_x = base_initial[i][j][0]+D_w_l_min_L0*math.cos(angle)
                shape_y = base_initial[i][j][1] + z_offset- D_w_l_min_L0 * math.sin(angle)-crush
                crush_e_min_group[i].append([shape_x,shape_y])

                shape_x = base_initial[i][j][0]+D_w_l_max_L0*math.cos(angle)
                shape_y = base_initial[i][j][1] + z_offset- D_w_l_max_L0 * math.sin(angle)-crush
                crush_e_max_group[i].append([shape_x,shape_y])

                shape_x = base_initial[i][j][0]+D_w_l_min*math.cos(angle)+Delta_Zmin* math.sin(angle)-abs(x_move)
                shape_y = base_initial[i][j][1]-D_w_l_min * math.sin(angle)+Delta_Zmin *math.cos(angle)+z_offset+abs(lift_stop)
                lift_e_min_group[i].append([shape_x,shape_y])

                shape_x = base_initial[i][j][0]+D_w_l_max*math.cos(angle)+Delta_Zmax* math.sin(angle)+abs(x_move)
                shape_y = base_initial[i][j][1]-D_w_l_max * math.sin(angle)+Delta_Zmax *math.cos(angle)+z_offset+abs(lift_stop)
                lift_e_max_group[i].append([shape_x,shape_y])

                shape_x = base_initial[i][j][0]+D_w_l_min*math.cos(angle)+Delta_Zmin* math.sin(angle)-abs(x_move)
                shape_y = base_initial[i][j][1]-D_w_l_min * math.sin(angle)+Delta_Zmin *math.cos(angle)+z_offset-abs(bump_stop)
                bump_e_min_group[i].append([shape_x,shape_y])

                shape_x = base_initial[i][j][0]+D_w_l_max*math.cos(angle)+Delta_Zmax* math.sin(angle)+abs(x_move)
                shape_y = base_initial[i][j][1]-D_w_l_max * math.sin(angle)+Delta_Zmax *math.cos(angle)+z_offset-abs(bump_stop)
                bump_e_max_group[i].append([shape_x,shape_y])


        tare_innermost =EclipseCalculationUtils.innermost(tare_e_min_group)
        tare_outermost =EclipseCalculationUtils.outermost(tare_e_max_group)
        crush_innermost =EclipseCalculationUtils.innermost(crush_e_min_group)
        crush_outermost =EclipseCalculationUtils.outermost(crush_e_max_group)
        static_group = [tare_innermost, tare_outermost, crush_innermost, crush_outermost]
        static_innermost=min(static_group,key=lambda static_group:static_group[0]**2+static_group[1]**2)
        static_outermost = max(static_group, key=lambda static_group: static_group[0] ** 2 + static_group[1] ** 2)
        initial_innermost =EclipseCalculationUtils.innermost(initial_group)
        initial_outermost =EclipseCalculationUtils.outermost(initial_group)
        lift_innermost =EclipseCalculationUtils.innermost(lift_e_min_group)
        lift_outermost =EclipseCalculationUtils.outermost(lift_e_max_group)
        bump_innermost =EclipseCalculationUtils.innermost(bump_e_min_group)
        bump_outermost =EclipseCalculationUtils.outermost(bump_e_max_group)

        "Circles of disc and friction radius of Odyssey"
        circle_outer = EclipseCalculationUtils.circle_array(disc_outer)
        circle_inner = EclipseCalculationUtils.circle_array(disc_inner)
        circle_rm=EclipseCalculationUtils.circle_array(R_m*2)
        circle_wheel_screw=EclipseCalculationUtils.circle_array(wheel_screw)


        inner_outer_points={
                            "static_innermost":static_innermost,"static_outermost":static_outermost,
                            "initial_innermost":initial_innermost,"initial_outermost": initial_outermost,
                            "lift_innermost": lift_innermost, "lift_outermost": lift_outermost,
                            "bump_innermost": bump_innermost, "bump_outermost": bump_outermost
                            }

        data_group={
                    "very_original_shape_data":shape_data_list,
                    "n_area":n_area,
                    "points_group":points_group,
                    "initial_group":initial_group,
                    # "initial_group":base_initial_divided,
                    "circle_outer":circle_outer,
                    "circle_inner":circle_inner,
                    "circle_wheel_screw":circle_wheel_screw,
                    "wheel_screw":wheel_screw/2,
                    "R_m":R_m,
                    "circle_rm":circle_rm,
                    "E_other":E_other,
                    "tare_e_min_group":tare_e_min_group,
                    "tare_e_max_group":tare_e_max_group,
                    "crush_e_min_group":crush_e_min_group,
                    "crush_e_max_group":crush_e_max_group,
                    "lift_e_min_group": lift_e_min_group,
                    "lift_e_max_group": lift_e_max_group,
                    "bump_e_min_group": bump_e_min_group,
                    "bump_e_max_group": bump_e_max_group,
                    "inner_outer_points":inner_outer_points
                    }
        return data_group
