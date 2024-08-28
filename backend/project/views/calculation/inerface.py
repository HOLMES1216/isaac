from abc import ABC, abstractmethod  

class BXActCalculatorBase(ABC):
    def __init__(self, E, angle, Pad_thickness, clearance, y_offset, Disc_Width, y_move,
                 disc_wear, pad_wear):
        self.E = E  # The installation reference dimension for Caliper/TBU
        self.angle = angle
        self.Pad_thickness = Pad_thickness
        self.clearance = clearance
        self.y_offset = y_offset
        self.Disc_Width = Disc_Width
        self.y_move = y_move
        self.disc_wear = disc_wear
        self.pad_wear = pad_wear

    @abstractmethod
    def transfer_list(self):
        pass
    @abstractmethod
    def transfer_list_instant(self):
        pass

class BXCalculationModeBase(ABC):

    @abstractmethod
    def calculation_results():
        pass
