from project.models import *
from project.views.calculation.service.generate_calculator import *
from functools import cached_property
import json

from project.views.calculation.dataclass import *

class BXCalculationSystem:

    def __init__(self,json_data):
        # data = json.loads(json_data)
        self.bogie_brake_system = BogieBrakeSystem(
            left_form=json_data["leftForm"],
            right_form=json_data["rightForm"],
            active_name=json_data["activeName"]
        )
        self.kwargs={}
        self.actuator_object=self.actuator_object
        self.pad_object=self.pad_object

    @cached_property
    def actuator_object(self):
        return Brake.objects.get(id=self.bogie_brake_system.actuator.caliperItem) 
       
    @cached_property
    def pad_object(self):
        return BrakeLiningShoe.objects.get(id=self.bogie_brake_system.pad.padId)    

    @cached_property
    def actuator_calculator(self):     
        # get Actuator object by ORM
        actuator_data=self.actuator_object
        actuator_type = self.bogie_brake_system.actuator.caliperType
        self.kwargs = {
            'E': self.bogie_brake_system.brakeCaliperPositioning.eDimension,
            'y_offset': self.bogie_brake_system.brakeCaliperPositioning.installationOffsetY,
            'angle': self.bogie_brake_system.brakeCaliperPositioning.rotationOfCaliper,
            'Disc_Width': self.bogie_brake_system.disc.discWidth,
            'y_move': self.bogie_brake_system.brakeCaliperPositioning.rotationOfCaliper,
            'disc_wear': self.bogie_brake_system.brakeCaliperPositioning.discWear,
            'pad_wear': self.bogie_brake_system.brakeCaliperPositioning.padWear,
            'clearance': self.bogie_brake_system.pad.clearance,
            'Pad_thickness': self.bogie_brake_system.pad.padThickness
            # Additional parameters for ClassicAct or CompactAct
        }
        
        if actuator_type == 'classic':
            additional_kwargs = {
                'Lever_length': actuator_data.lever_length,
                'LLF': actuator_data.lever_length_the_front,
                'Offset_Lever': actuator_data.offset_pull_rod_rotation_point_in_lever,
                'PHH': actuator_data.pad_holder_height,
                'WLB': actuator_data.wear_of_lever_bolt,
                'WPHB': actuator_data.wear_of_pad_holder_bolt,
                'DCY': actuator_data.distance_cylinder_fixation_yoke_fixation,
                'PAC': actuator_data.pre_adjustment_in_cylinder,
                'G_dimension': actuator_data.gdimension,
                'HTL': actuator_data.hanger_upper_bolt_to_lower_bolt,
                'BFH': actuator_data.hanger_lower_bolt_to_pad_holder_assemble_surface,
                'DHB': actuator_data.dis_between_hanger_upper_bolt,
                'HUTC': actuator_data.hanger_upper_bolt_to_caliper_center,
                'HLPC': actuator_data.hanger_lower_bolt_to_pad_center,
            }
            self.kwargs.update(additional_kwargs)

            return ClassicActCalculator(**self.kwargs)


        elif actuator_type == 'compact':
            additional_kwargs = {
                'LL': actuator_data.ll,
                'LR': actuator_data.lr,
                'LR1': actuator_data.lr1,
                'LR2': actuator_data.lr2,
                'D1': actuator_data.d1,
                'D2': actuator_data.d2,
                'D3': actuator_data.d3,
                'H1': actuator_data.h1,
                'H2': actuator_data.h2,
                'H3': actuator_data.h3,
                'Side': self.bogie_brake_system.extraSettings.sideReference,
            }
            self.kwargs.update(additional_kwargs)

            return CompactActCalculator(**self.kwargs)
        
    @property
    def pad_shape(self):
        return json.loads(self.pad_object.pad_shape)       
    
    @property
    def F_point(self):
        item_name=self.pad_object.item_name
        return float(item_name.split("_")[-1])
