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



class GraverCalculation(BXCalculationModeBase):
    def __init__(self,bxCalculationSystem:BXCalculationSystem) -> None:
        super().__init__()
        self.bxCalculationSystem=bxCalculationSystem

    def calculation_results(self):

        """
        Calculation Setting
        """
        P_tol=0.00001
        step_cal=1

        """ 
            Basic Inputs for Static Positioning and Dynamic 
        """

        "static position"
        E_dimension = self.bxCalculationSystem.bogie_brake_system.brakeCaliperPositioning.eDimension
        angle = self.bxCalculationSystem.bogie_brake_system.brakeCaliperPositioning.rotationOfCaliper
        z_offset = self.bxCalculationSystem.bogie_brake_system.brakeCaliperPositioning.installationOffsetZ
        "dynamic movement"
        'movement'
        x_move= self.bxCalculationSystem.bogie_brake_system.kinematicPrimarySuspension.X_LongitudinalMovement
        crush = self.bxCalculationSystem.bogie_brake_system.kinematicPrimarySuspension.C_TareDatumToCrushDatum
        Tare_amp = self.bxCalculationSystem.bogie_brake_system.kinematicPrimarySuspension.E_AmplitudeTare
        Crush_amp = self.bxCalculationSystem.bogie_brake_system.kinematicPrimarySuspension.D_AmplitudeCrush

        "disc selection"
        disc_inner=self.bxCalculationSystem.bogie_brake_system.disc.discInnerDiameter
        disc_outer = self.bxCalculationSystem.bogie_brake_system.disc.discOuterDiameter
        Disc_Width = self.bxCalculationSystem.bogie_brake_system.disc.discWidth

        "pad selection"

        shape_data=self.bxCalculationSystem.pad_shape

        """ 
            Specific Settings and offsets calculation due to caliper movement/wear
        """

        "offset due to caliper movement/wear"

        instantdata=self.bxCalculationSystem.actuator_calculator.transfer_list
        Delta_Z = instantdata.Delta_Z
        D_w_l_min = instantdata.D_w_l_min
        D_w_l_max = instantdata.D_w_l_max

        """
        Calculation for this mode
        """

        "Inital position calculation"
        F_point=self.bxCalculationSystem.F_point
        F_offset=E_dimension-F_point
        angle = angle * math.pi / 180
        Long_1=x_move

        P_tol_divide = 0.08
        list = shape_data
        n_area = int(list[0][3])
        points_group = []
        points_group_divided = []
        base_initial_no_rotate = [[] for i in range(n_area)]

        n_lower = 4 + n_area
        base_initial_divided = [[] for i in range(n_area)]
        for i in range(0, n_area):
            n_points = int(list[0][4 + i])
            points_group.append(n_points)
            for j in range(0, n_points):
                base_initial_no_rotate[i].append([list[0][j + n_lower] + F_offset, list[1][j + n_lower]])
            n_lower = n_lower + n_points

        i = 0
        j = 1

        while i < n_area:
            n_points = points_group[i]
            PX1 = base_initial_no_rotate[i][0][0]
            PY1 = base_initial_no_rotate[i][0][1]
            shape_x = PX1 * math.cos(angle) + (PY1 + Delta_Z) * math.sin(angle)
            shape_y = -1 * PX1 * math.sin(angle) + (PY1 + Delta_Z) * math.cos(angle)
            base_initial_divided[i].append([shape_x, shape_y])
            points_group_divided.append(1)
            while j < n_points - 1:
                PX0 = base_initial_no_rotate[i][j - 1][0]
                PY0 = base_initial_no_rotate[i][j - 1][1]
                PX1 = base_initial_no_rotate[i][j][0]
                PY1 = base_initial_no_rotate[i][j][1]
                PX2 = base_initial_no_rotate[i][j + 1][0]
                PY2 = base_initial_no_rotate[i][j + 1][1]
                if abs((PX2 - PX1) * (PX1 - PX0)) > P_tol_divide ** 2:
                    if abs((PY2 - PY1) / (PX2 - PX1) - (PY1 - PY0) / (PX1 - PX0)) > P_tol_divide:
                        shape_x = PX1 * math.cos(angle) + (PY1 + Delta_Z) * math.sin(angle)
                        shape_y = -1 * PX1 * math.sin(angle) + (PY1 + Delta_Z) * math.cos(angle)
                        base_initial_divided[i].append([shape_x, shape_y])
                        points_group_divided[i] = points_group_divided[i] + 1
                        if (abs(PX2 - PX1) + abs(PY2 - PY1)) < 0.0001:
                            j = j + 1
                else:
                    if abs(PX2 - PX1) + abs(PX1 - PX0) > P_tol_divide:
                        shape_x = PX1 * math.cos(angle) + (PY1 + Delta_Z) * math.sin(angle)
                        shape_y = -1 * PX1 * math.sin(angle) + (PY1 + Delta_Z) * math.cos(angle)
                        base_initial_divided[i].append([shape_x, shape_y])
                        points_group_divided[i] = points_group_divided[i] + 1
                        if (abs(PX2 - PX1) + abs(PY2 - PY1)) < 0.0001:
                            j = j + 1
                j += 1
            PX1 = base_initial_no_rotate[i][n_points - 1][0]
            PY1 = base_initial_no_rotate[i][n_points - 1][1]
            shape_x = PX1 * math.cos(angle) + (PY1 + Delta_Z) * math.sin(angle)
            shape_y = -1 * PX1 * math.sin(angle) + (PY1 + Delta_Z) * math.cos(angle)
            base_initial_divided[i].append([shape_x, shape_y])
            points_group_divided[i] = points_group_divided[i] + 1
            j = 1
            i += 1

        R_step = []
        upper = int((disc_outer / 2 - round(disc_inner / 2)) * (1 / step_cal) + 1)
        for i in range(upper):
            R_step.append(disc_inner / 2 + i)
        r_x = [[0, 0] for i in range(len(R_step))]

        E_step = []
        upper = round((D_w_l_max - D_w_l_min) * (1 / step_cal) + 1)
        upper = int(upper)
        for i in range(upper):
            E_step.append(round(D_w_l_min + i * step_cal))

        NX_step = []
        Nx_min = -1 * abs(Long_1) + D_w_l_min * math.cos(angle)
        Nx_max = abs(Long_1) + D_w_l_max * math.cos(angle)
        upper = round((Nx_max - Nx_min) * (1 / step_cal) + 1)
        upper = int(upper)

        for i in range(upper):
            NX_step.append(round(Nx_min + i * step_cal))

        NTare_amp_step = []
        Nx_min = -1 * abs(Tare_amp) - D_w_l_max * math.sin(angle)
        Nx_max = abs(Tare_amp) - D_w_l_min * math.sin(angle)
        upper = round((Nx_max - Nx_min) * (1 / step_cal) + 1)
        upper = int(upper)
        for i in range(upper):
            NTare_amp_step.append(round(Nx_min + i * step_cal))

        NCrush_amp_step = []
        Nx_min = -1 * abs(Crush_amp) - D_w_l_max * math.sin(angle) - abs(crush)
        Nx_max = abs(Crush_amp) - D_w_l_min * math.sin(angle) - abs(crush)
        upper = round((Nx_max - Nx_min) * (1 / step_cal) + 1)
        upper = int(upper)
        for i in range(upper):
            NCrush_amp_step.append(round(Nx_min + i * step_cal))

        Group_step = [R_step, E_step, NX_step, NTare_amp_step, NCrush_amp_step]

        Group_X_Set = []
        Sum_X = 0
        Error_set = []

        for i_TTC in range(2):
            for i_x in range(len(NX_step)):
                # for i_x in range(1):
                #     print(NX_step[i_x])
                if i_TTC == 0:
                    Znn = len(NTare_amp_step)
                else:
                    Znn = len(NCrush_amp_step)
                for i_Z in range(Znn):
                    if i_TTC == 0:
                        Z_ap = NTare_amp_step[i_Z]
                    else:
                        Z_ap = NCrush_amp_step[i_Z]
                    P_x_d_t2 = [[] for i in range(n_area)]
                    for i_area in range(n_area):
                        n_points = points_group_divided[i_area]
                        for j_point in range(n_points):
                            shape_x = base_initial_divided[i_area][j_point][0] + NX_step[i_x]
                            shape_y = base_initial_divided[i_area][j_point][1] + Z_ap + z_offset
                            P_x_d_t2[i_area].append([shape_x, shape_y])
                    for I in range(len(R_step)):
                        r_x[I][0] = R_step[I]
                        State_P = 0
                        kkkkk = 0
                        Group_X_Set = []
                        while (State_P == 0):
                            for i_area in range(n_area):
                                n_points = points_group_divided[i_area]
                                for j_point in range(n_points - 1):
                                    Group_X = self.Intersection_Q(
                                                                    P_x_d_t2[i_area][j_point][0],
                                                                    P_x_d_t2[i_area][j_point][1],
                                                                    P_x_d_t2[i_area][j_point + 1][0],
                                                                    P_x_d_t2[i_area][j_point + 1][1],
                                                                    R_step[I], P_tol / 10)
                                    if Group_X[0] == 1000:
                                        R_step[I] = P_tol * 100 + R_step[I]
                                        # print(R_step[I])
                                        kkkkk = 0
                                        break
                                    if Group_X[0] != -1000:
                                        kkkkk = kkkkk + 1
                                        # if R_step[I] == 247.002 or R_step[I]==247 :
                                        #     if i_x == 2 and i_Z == 9:
                                        #         print(f"Group:{Group_X} R:{R_step[I]}")
                                        Group_X_Set.extend(Group_X)
                            if len(Group_X_Set) % 2 == 0:
                                State_P = 1
                            else:
                                Error_set.append(R_step[I])
                                R_step[I] = P_tol * 100 + R_step[I]
                                # print(R_step[I])
                                # print(Group_X_Set)
                                Group_X_Set = []

                        if kkkkk == 0:
                            Sum_X = 0
                        else:
                            Group_X_Set.sort(reverse=True)
                            Sum_X = 0

                            for count_x in range(0, len(Group_X_Set), 2):
                                Sum_X = Sum_X + Group_X_Set[count_x] - Group_X_Set[count_x + 1]

                            PPP = 0
                            if i_TTC == 0:
                                for E_j in range(len(E_step)):
                                    PPP = PPP + self.P_XYZ(0, Long_1,NX_step[i_x] - E_step[E_j] * math.cos(angle)) * \
                                          self.P_XYZ(0, Tare_amp,Z_ap + E_step[E_j] * math.sin(angle)) * \
                                          abs(1 / len(E_step)) * step_cal
                            else:
                                for E_j in range(len(E_step)):
                                    PPP = PPP + self.P_XYZ(0, Long_1,NX_step[i_x] - E_step[E_j] * math.cos(angle)) * \
                                          self.P_XYZ(0, Crush_amp,Z_ap + E_step[E_j] * math.sin(angle)) * \
                                          abs(1 / len(E_step)) * step_cal
                            r_x[I][1] = Sum_X * PPP * step_cal + r_x[I][1]

        V_T = 40000000
        V_wear = 0
        for I in range(len(r_x)):
            V_wear = V_wear + 2 * 3.14 * r_x[I][0] * r_x[I][1]

        V_T_T = V_T / V_wear
        V_wear = 0

        min_temp = 0
        for I in range(len(r_x)):
            r_x[I][1] = r_x[I][1] * V_T_T
            V_wear = V_wear + 2 * 3.14 * r_x[I][0] * r_x[I][1]
            r_x[I][1] = -r_x[I][1] / 3 - 45
            if r_x[I][1] < min_temp:
                min_temp = r_x[I][1]
            r_x[I][1] = r_x[I][1] + 300

        sum_D = round(abs(min_temp + 45) * 3 / 39, 2)

        list_result = {
            "n_area": n_area,
            "points_group": points_group,
            "base_initial_divided": base_initial_divided,
            "points_group_divided": points_group_divided,
            "R_step": R_step,
            "r_x": r_x,
            "Group_step": Group_step,
            "sum_D": sum_D,
            "Error_set": Error_set,
            "Error_set_len": len(Error_set)
        }

        return list_result

    @staticmethod
    def Intersection_Q(PPX1,PPY1,PPX2,PPY2,RRk,E_A):
        T_Temp=[]
        PPA = (PPX2 - PPX1)** 2 + (PPY2 - PPY1) ** 2
        PPB = 2 * PPX1 * (PPX2 - PPX1) + 2 * PPY1 * (PPY2 - PPY1)
        PPC = PPX1 ** 2 + PPY1 ** 2 - RRk ** 2
        Delta_I = PPB ** 2 - 4 * PPA * PPC
        if Delta_I<0:
            T_Temp.append(-1000)
        elif Delta_I<=E_A and Delta_I >= 0:
            PPt1 = -PPB / (2 * PPA)
            if PPt1>1 or PPt1 < 0:
                T_Temp.append(-1000)
            elif PPt1 <= 1 and PPt1 >= 1 - E_A or PPt1 >= 0 and PPt1 <= E_A:
                T_Temp.append(1000)
            else:
                Deg_1=math.atan((PPY1 + PPt1 * (PPY2 - PPY1)) / (PPX1 + PPt1 * (PPX2 - PPX1)))
                T_Temp.append(Deg_1*180/math.pi)
                T_Temp.append(Deg_1 * 180 / math.pi)
        else:
            PPt1 = 1 / (2 * PPA) * (-PPB - Delta_I ** 0.5)
            PPt2 = 1 / (2 * PPA) * (-PPB + Delta_I ** 0.5)
            if PPt1 <= 1 and PPt1 >= 1 - E_A or PPt1 >= 0 and PPt1 <= E_A or PPt2 <= 1 and PPt2 >= 1 - E_A or PPt2 >= 0 and PPt2 <= E_A:
                T_Temp.append(1000)
            elif (PPt1 > 1 or PPt1 < 0) and (PPt2 > 1 or PPt2 < 0):
                T_Temp.append(-1000)
            elif (PPt1 < 1 - E_A and PPt1 > E_A) and (PPt2 > 1 or PPt2 < 0):
                Deg_1 = math.atan((PPY1 + PPt1 * (PPY2 - PPY1)) / (PPX1 + PPt1 * (PPX2 - PPX1)))
                T_Temp.append(Deg_1 * 180 / math.pi)
            elif (PPt2 < 1 - E_A and PPt2 > E_A) and (PPt1 > 1 or PPt1 < 0):
                Deg_1 = math.atan((PPY1 + PPt2 * (PPY2 - PPY1)) / (PPX1 + PPt2 * (PPX2 - PPX1)))
                T_Temp.append(Deg_1 * 180 / math.pi)
            elif (PPt2 < 1 - E_A and PPt2 > E_A) and (PPt1 < 1 - E_A and PPt1 > E_A):
                Deg_1 = math.atan((PPY1 + PPt1 * (PPY2 - PPY1)) / (PPX1 + PPt1 * (PPX2 - PPX1)))
                Deg_2 = math.atan((PPY1 + PPt2 * (PPY2 - PPY1)) / (PPX1 + PPt2 * (PPX2 - PPX1)))
                T_Temp.append(Deg_1 * 180 / math.pi)
                T_Temp.append(Deg_2 * 180 / math.pi)
        return T_Temp
    @staticmethod
    def P_XYZ(PU, AM, xyz):
        if xyz<-1*AM+PU or xyz>AM+PU:
            normal_num=0
        else:
            e = 2.7182818
            pi = 3.1415926
            standard_dev=AM/1.6
            normal_num = e ** (-((xyz - PU) ** 2) / (2 * standard_dev ** 2)) / (standard_dev * (2 * pi) ** 0.5)
        return normal_num

