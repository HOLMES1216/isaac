import json
from dataclasses import dataclass

@dataclass
class Component:
    pass

@dataclass
class Actuator(Component):
    caliperType: str
    caliperDetailType: str
    caliperItem: str

@dataclass
class Disc(Component):
    discInnerDiameter: float
    discOuterDiameter: float
    discWidth: float

@dataclass
class Wheel(Component):
    wheelInnerDiameter: float

@dataclass
class Pad(Component):
    padId: int  # padId
    padThickness: float
    clearance: float

@dataclass
class BrakeCaliperPositioning(Component):
    eDimension: float
    installationOffsetY: float  # installationOffsetY
    installationOffsetZ: float  # installationOffsetZ
    rotationOfCaliper: float  # rotationOfCaliper
    discWear: float
    padWear: float

@dataclass
class KinematicPrimarySuspension(Component):
    X_LongitudinalMovement: float  # x_LongitudinalMovement
    Y_LateralMovement: float  # y_LateralMovement
    A_TareDatumToLiftStop: float  # a_TareDatumToLiftStop
    B_TareDatumToBumpStop: float  # b_TareDatumToBumpStop
    C_TareDatumToCrushDatum: float  # C_TareDatumToCrushDatum
    D_AmplitudeCrush: float  # D_AmplitudeCrush
    E_AmplitudeTare: float  # E_AmplitudeTare
    discWearStart: float
    discWearEnd: float
    wearOfLeverBolt: float
    wearOfPadHolderBolt: float

@dataclass
class FunctionalInputs(Component):
    inputs: dict

@dataclass
class ExtraSettings(Component):
    sideReference: str
    wheelSettingMode: str


@dataclass
class BogieBrakeSystem:
    left_form: dict
    right_form: dict
    active_name: str

    def __post_init__(self):
        try:
            # 提取并初始化组件
            self.actuator = Actuator(
                caliperType=self.left_form['caliperType'],
                caliperDetailType=self.left_form['caliperDetailType'],
                caliperItem=self.left_form['caliperProduct']
            )
            self.disc = Disc(
                discInnerDiameter=float(self.left_form['discInnerDiameter']),
                discOuterDiameter=float(self.left_form['discOuterDiameter']),
                discWidth=float(self.left_form['discWidth'])
            )
            self.wheel = Wheel(
                wheelInnerDiameter=float(self.left_form['wheelInnerDiameter'])
            )
            self.pad = Pad(
                padId=int(self.left_form['padProduct']),  # 将 padProduct 转换为整数
                padThickness=float(self.left_form['padThickness']),
                clearance=float(self.left_form['clearance'])
            )
            self.brakeCaliperPositioning = BrakeCaliperPositioning(
                eDimension=float(self.left_form['eDimension']),
                installationOffsetY=float(self.left_form['ioy']),
                installationOffsetZ=float(self.left_form['ioz']),
                rotationOfCaliper=float(self.left_form['roc']),
                discWear=float(self.left_form['discWear']),
                padWear=float(self.left_form['padWear'])
            )
            self.kinematicPrimarySuspension = KinematicPrimarySuspension(
                X_LongitudinalMovement=float(self.left_form['xlm']),
                Y_LateralMovement=float(self.left_form['ylm']),
                A_TareDatumToLiftStop=float(self.left_form['atd']),
                B_TareDatumToBumpStop=float(self.left_form['btd']),
                C_TareDatumToCrushDatum=float(self.left_form['ctd']),
                D_AmplitudeCrush=float(self.left_form['dac']),
                E_AmplitudeTare=float(self.left_form['eat']),
                discWearStart=float(self.left_form['discWearStart']),
                discWearEnd=float(self.left_form['discWearEnd']),
                wearOfLeverBolt=float(self.left_form['wearOfLeverBolt']),
                wearOfPadHolderBolt=self.left_form['wearOfPadHolderBolt']
            )
            self.extraSettings = ExtraSettings(
                sideReference=self.left_form['sideReference'],
                wheelSettingMode=self.left_form['wheelSettingMode']
            )
            self.functionalInputs = FunctionalInputs(
                inputs=self.right_form
            )
        except KeyError as e:
            print(f"Missing key in form data: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

@dataclass  
class TransferResult:  
    G: float  
    R: float  
    E_other: float  
    D_w_l_min: float  
    D_w_l_max: float  
    Delta_Z: float  
    Delta_Zmax: float  
    Delta_Zmin: float  
    D_w_l_min_L0: float  
    D_w_l_max_L0: float  
    D_w_l_w_min: float  
    D_w_l_w_max: float  
    Delta_Z_D_min: float  
    Delta_Z_D_max: float  
    comment: str  
  
@dataclass  
class TransferInstantResult:  
    Delta_Z: float  
    D_w_l_Instant: float  
    Delta_Z_Instant: float

