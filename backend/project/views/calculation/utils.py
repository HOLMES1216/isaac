from abc import ABC, abstractmethod  
from collections import namedtuple
from project.models import *
import numpy as np
class EclipseCalculationUtils:
    @staticmethod
    def Rm_cal(P_points, P_XY, E_dim, E_delta_Rm, V_Rm):
        # a_com_rm = 0
        # r_sx_rm = 0
        # I_y_rm = 0
        # n_area=len(P_points)

        # for i in range(0, n_area):
        #     n_points = P_points[i]
        #     for j in range(0, n_points):
        #         P_XY[i][j][0] = P_XY[i][j][0] + E_delta_Rm
        #         P_XY[i][j][1] = P_XY[i][j][1] + V_Rm

        # for i in range(0, n_area):
        #     n_points = P_points[i]
        #     for j in range(0, n_points - 1):

        #         d_x_i_rm = P_XY[i][j + 1][0] - P_XY[i][j][0]
        #         d_y_i_rm = (P_XY[i][j + 1][1] + P_XY[i][j][1]) / 2
        #         r_sx_i_rm = (P_XY[i][j + 1][0] + P_XY[i][j][0]) / 2
        #         r_sy_i_rm = (P_XY[i][j + 1][1] + P_XY[i][j][1]) / 4
        #         a_i_rm = d_x_i_rm * d_y_i_rm
        #         a_com_rm = a_com_rm + a_i_rm
        #         r_sx_rm = r_sx_rm + r_sx_i_rm * a_i_rm
        #         I_y_i_rm = d_y_i_rm * d_x_i_rm ** 3 / 12
        #         I_y_rm = I_y_i_rm + I_y_rm + r_sx_i_rm ** 2 * a_i_rm

        # r_sx_rm = r_sx_rm / a_com_rm
        # I_y_rm = I_y_rm - r_sx_rm ** 2 * a_com_rm


        # Rm = 0
        # n_p_rm = 30
        # r_fx_rmm = E_dim+ E_delta_Rm
        # for i in range(0, n_area):
        #     n_points = P_points[i]
        #     for j in range(0, n_points - 1):
        #         d_x_i_rm = (P_XY[i][j + 1][0] - P_XY[i][j][0]) / n_p_rm
        #         d_y_i_rm = (P_XY[i][j + 1][1] + P_XY[i][j][1]) / (2 * n_p_rm)
        #         a_i_rm = d_x_i_rm * d_y_i_rm

        #         for l_rm in range(0, n_p_rm):
        #             r_sx_i_rm = P_XY[i][j][0] + d_x_i_rm * (l_rm + 0.5)
        #             for k_rm in range(0, n_p_rm):
        #                 r_sy_i_rm = d_y_i_rm * (k_rm + 0.5)
        #                 lamda_rm = (1 / a_com_rm + (r_fx_rmm - r_sx_rm) * (r_sx_i_rm - r_sx_rm) / I_y_rm) * (r_sx_i_rm ** 2 + r_sy_i_rm ** 2) ** 0.5
        #                 Rm = Rm + lamda_rm * a_i_rm
        # Rm = round(Rm, 1)
        P_XY = np.array(P_XY)
        P_XY[:, :, 0] += E_delta_Rm
        P_XY[:, :, 1] += V_Rm
        a_com_rm = 0
        r_sx_rm = 0
        I_y_rm = 0
        
        for i in range(len(P_points)):
            n_points = P_points[i]
            d_x_i_rm = P_XY[i, 1:n_points, 0] - P_XY[i, :n_points-1, 0]
            d_y_i_rm = (P_XY[i, 1:n_points, 1] + P_XY[i, :n_points-1, 1]) / 2
            r_sx_i_rm = (P_XY[i, 1:n_points, 0] + P_XY[i, :n_points-1, 0]) / 2
            r_sy_i_rm = (P_XY[i, 1:n_points, 1] + P_XY[i, :n_points-1, 1]) / 4
            a_i_rm = d_x_i_rm * d_y_i_rm
            a_com_rm += np.sum(a_i_rm)
            r_sx_rm += np.sum(r_sx_i_rm * a_i_rm)
            I_y_i_rm = d_y_i_rm * d_x_i_rm ** 3 / 12
            I_y_rm += np.sum(I_y_i_rm + r_sx_i_rm ** 2 * a_i_rm)
        
        r_sx_rm /= a_com_rm
        I_y_rm -= r_sx_rm ** 2 * a_com_rm
        
        Rm = 0
        n_p_rm = 30
        r_fx_rmm = E_dim + E_delta_Rm
        
        for i in range(len(P_points)):
            n_points = P_points[i]
            d_x_i_rm = (P_XY[i, 1:n_points, 0] - P_XY[i, :n_points-1, 0]) / n_p_rm
            d_y_i_rm = (P_XY[i, 1:n_points, 1] + P_XY[i, :n_points-1, 1]) / (2 * n_p_rm)
            a_i_rm = d_x_i_rm * d_y_i_rm
            
            for l_rm in range(n_p_rm):
                r_sx_i_rm = P_XY[i, :n_points-1, 0] + d_x_i_rm * (l_rm + 0.5)
                for k_rm in range(n_p_rm):
                    r_sy_i_rm = d_y_i_rm * (k_rm + 0.5)
                    lamda_rm = (1 / a_com_rm + (r_fx_rmm - r_sx_rm) * (r_sx_i_rm - r_sx_rm) / I_y_rm) * np.sqrt(r_sx_i_rm ** 2 + r_sy_i_rm ** 2)
                    Rm += np.sum(lamda_rm * a_i_rm)
  
        Rm = round(Rm, 1)

        return Rm

    @staticmethod
    def innermost(array_group):
        # point = min(list(map(lambda x: min(x, key=lambda x: x[0] ** 2 + x[1] ** 2), array_group)),
        #                     key=lambda x: x[0] ** 2 + x[1] ** 2)
        # return point
        concatenated = np.concatenate(array_group)  

        distances_squared = concatenated[:, 0]**2 + concatenated[:, 1]**2  
 
        min_index = np.argmin(distances_squared)  

        return concatenated[min_index].tolist()  
    
    @staticmethod
    def outermost(array_group):
        # point = max(list(map(lambda x: max(x, key=lambda x: x[0] ** 2 + x[1] ** 2), array_group)),
        #                     key=lambda x: x[0] ** 2 + x[1] ** 2)
        # return point
  
        concatenated = np.concatenate(array_group)  
  
        distances_squared = concatenated[:, 0]**2 + concatenated[:, 1]**2  
 
        max_index = np.argmax(distances_squared)  

        return concatenated[max_index].tolist()   
    @staticmethod
    def get_distance_message(distance, d, type):  
        diff = distance - d / 2  
        if type == 'Inner Diameter':  
            diff = -diff  
        return f"{type} {'overlap ' + str(round(diff, 2)) if diff > 0 else 'gap ' + str(round(-diff, 2))}mm" 
     
    @staticmethod
    def refresh_distance_message(distance_min,distance_max,disc_outer,disc_inner,wheelInnerDiameter):  
        # 假设存在一个全局的state字典，这里只是示例，具体实现可能不同  
        state = {}  
        state['distanceMsg']['msgID'] = EclipseCalculationUtils.get_distance_message(distance_min, disc_inner, 'Inner Diameter')  
        state['distanceMsg']['msgOD'] = EclipseCalculationUtils.get_distance_message(distance_max, disc_outer, 'Outer Diameter')  
        state['distanceMsg']['msgWD'] = EclipseCalculationUtils.get_distance_message(distance_max, wheelInnerDiameter, 'Wheel Diameter')  
        
        return state
    

     
    @staticmethod
    def circle_array(diameter):

        radius = diameter / 2
        # 创建一个从0到1的100个点的数组
        theta = np.linspace(0, 2 * np.pi, 100)
        # 计算圆上的点的坐标
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        # 将计算结果转换为列表
        array_circle = list(zip(x, y))

        return array_circle

